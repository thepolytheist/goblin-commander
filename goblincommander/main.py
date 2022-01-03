import os
import sys
from enum import Enum
from random import randint, choices, choice
from typing import Any

from termcolor import colored

from creature_groups import Horde
from creatures import Goblin, GoblinCommander
from intro import print_title_figure, show_prelude
from menus import show_game_menu, show_main_menu, show_raid_menu, show_scout_menu, show_name_menu, show_name_input, \
    show_title_menu
from settlements import Settlement, NomadEncampment, QuietVillage, BusyTown, BustlingCity, GleamingCastle
from stash import Stash
from stats import StatKey


class StateKey(str, Enum):
    COMMANDER = "commander"
    HORDE = "horde"
    SETTLEMENTS = "settlements"
    STASH = "stash"
    WEEK = "week"


state: dict[StateKey, Any] = {}


def clear():
    """Pushes old content off the top of the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_stash():
    stash = state[StateKey.STASH]
    print(f"You have {stash.food} food and {stash.gold} gold remaining in your stash.")


def pass_weeks(n: int, dry_run=False) -> bool:
    horde_upkeep = state[StateKey.HORDE].get_upkeep()
    stash = state[StateKey.STASH]

    if horde_upkeep.gold * n > stash.gold or horde_upkeep.food * n > stash.food:
        print("You will need a bigger stash for that. "
              f"Maintaining your horde for {n} week(s) will require {horde_upkeep.gold * n} gold "
              f"and {horde_upkeep.food * n} food.\n"
              f"Current stash: {stash.gold} gold, {stash.food} food.")
        return False

    if not dry_run:
        stash.gold -= horde_upkeep.gold * n
        stash.food -= horde_upkeep.food * n
        state[StateKey.WEEK] += n
        print(f"{n} week(s) have passed. In this time, your horde has required {horde_upkeep.gold * n} gold "
              f"and {horde_upkeep.food * n} food to stay happy.")
    return True


def raid(horde: Horde, settlement: Settlement) -> Settlement:
    if settlement.defeated or not settlement.militia:
        raise ValueError("Raid target is not a valid settlement for raiding.")

    # TODO: Refactor this process for testability

    horde_beef = horde.get_stat_sum(StatKey.BEEF)

    militia_beef = settlement.militia.get_stat_sum(StatKey.BEEF)
    militia_cunning = settlement.militia.get_stat_sum(StatKey.CUNNING)

    print(settlement.description)

    print(f"\nBase horde Beef: {horde_beef:.2f}")
    print(f"Base militia Beef: {militia_beef:.2f}\n")

    if horde.get_stat_avg(StatKey.REPUTATION) > 4.5:
        print(f"[REP] ", end="")
        modifier_string = colored(f"(-{militia_cunning * 0.3:.2f} militia Cunning)", "green")
        militia_cunning *= 0.7
        print(f"The {settlement.name} defense is losing their wits in the face of your famous might. {modifier_string}")

    print("[QCK] ", end="")
    if horde.get_stat_avg(StatKey.QUICKNESS) > settlement.militia.get_stat_avg(StatKey.QUICKNESS):
        modifier_string = colored(f"(-{militia_beef * 0.1:.2f} militia Beef)", "green")
        print(f"Your speedy horde got the drop on the {settlement.name} defenses! You've caught them unprepared. "
              f"{modifier_string}")
        militia_beef *= 0.9
    else:
        if settlement.scouted:
            print(f"The {settlement.name} militia rallied quickly,"
                  " but your scouts found a critical flaw in their defenses. Not to worry. (No change)")
        else:
            modifier_string = colored(f"(-{horde_beef * 0.1:.2f} horde Beef)", "red")
            print(f"Uh oh. The {settlement.name} defenses rallied their forces in record time."
                  f" You've got your work cut out for you. {modifier_string}")
            horde_beef *= 0.9

    # Need to use local militia cunning to allow for modification
    print("[CUN] ", end="")
    if settlement.scouted or horde.get_stat_avg(StatKey.CUNNING) > militia_cunning / len(settlement.militia.members):
        modifier_string = colored(f"(+{horde_beef * 0.1:.2f} horde Beef)", "green")
        if settlement.scouted:
            print(f"The information from your scouts has given you the tactical edge. {modifier_string}")
        else:
            print(f"The {settlement.name} defenses don't seem too bright. Let's show them who's boss. "
                  f"{modifier_string}")
        horde_beef *= 1.1
    else:
        modifier_string = colored(f"(+{militia_beef * 0.1:.2f} militia Beef)", "red")
        print(f"Hmm. These men defending {settlement.name} are smarter than we thought."
              f" Best keep our heads on straight. {modifier_string}")
        militia_beef *= 1.1

    print(f"\nAdjusted horde Beef: {horde_beef:.2f}")
    print(f"Adjusted militia Beef: {militia_beef:.2f}\n")
    if horde_beef > militia_beef:
        print(colored("VICTORY", "green"))
        print(f"Your horde defeated the pitiful defenses of {settlement.name}.")
        settlement.defeated = True
        settlement.militia.members = []
        horde.bolster(1, 3)
    else:
        print(colored("DEFEAT", "red"))
        print(f"Your pitiful horde was defeated by the defenses of {settlement.name}. "
              "Half of them didn't make it back.")
        horde.members = [m for i, m in enumerate(horde.members) if i % 2 == 0 or m.is_commander]
    return settlement


def raid_menu():
    print(f"Your horde currently has {state[StateKey.HORDE].get_stat_sum(StatKey.BEEF)} Beef.")
    selection = show_raid_menu(state[StateKey.SETTLEMENTS])

    match selection:
        case Settlement() as s:
            pass_weeks(1)
            clear()
            print(colored("\nRAID", "blue"))
            print(f"You've chosen to raid {s.name}.")
            s = raid(state[StateKey.HORDE], s)
            if s.defeated:
                print(f"Your successful raid added {s.reward.food} food and {s.reward.gold} gold to the stash.")
                state[StateKey.STASH].add(s.reward)


def scout_menu():
    print(f"Your horde currently has {state[StateKey.HORDE].get_stat_sum(StatKey.BEEF)} Beef.")
    selection = show_scout_menu(state[StateKey.SETTLEMENTS])

    match selection:
        case Settlement() as s:
            pass_weeks(1)
            clear()
            print(colored("\nSCOUT", "blue"))
            s.scouted = True
            print(f"Your scouts have gained valuable info about {s.name}:")
            print(f"Beef: {s.militia.get_stat_sum(StatKey.BEEF)}, "
                  f"reward: {s.reward.food} food, {s.reward.gold} gold")


def recruit(commander: GoblinCommander):
    reputation = commander.stats[StatKey.REPUTATION].value
    print()
    if reputation == 5.0:
        print(f"No goblin is more feared or admired than {commander.name} the {commander.adjective}. "
              "Other creatures are running to join your famous horde.")
        state[StateKey.HORDE].bolster(4, 5)
    elif reputation > 4.0:
        print(f"The name {state[StateKey.COMMANDER].name} is known far and wide. "
              "With your charisma and notoriety, you've managed to recruit more creatures.")
        state[StateKey.HORDE].bolster(3, 4)
    elif reputation > 3.0:
        print(f"Creatures in the area are beginning to recognize the name {commander.name}. "
              "They don't need a lot of convincing to come fight for you.")
        state[StateKey.HORDE].bolster(2, 4)
    elif reputation > 2.0:
        print(f"No one's heard of {commander.name} the {commander.adjective}, "
              "but there are still some creatures looking for work.")
        state[StateKey.HORDE].bolster(1, 3)
    elif reputation > 1.0:
        print(f"{commander.name} the {commander.adjective} is known more for struggling and losing than anything else."
              " Regardless, you might be able to convince some creatures to follow you.")
        state[StateKey.HORDE].bolster(1, 2)
    else:
        # reputation < 1.0
        print(f"Good luck finding anyone who wants to join the unlucky horde of {commander.name} the Fallible.")
        state[StateKey.HORDE].bolster(0, 1)


def game_menu():
    print(f"\nWeek {state[StateKey.WEEK]}")
    show_stash()
    selection = show_game_menu()

    match selection:
        case "raid":
            # This needs to be a check only since there's a submenu
            if pass_weeks(1, dry_run=True):
                raid_menu()
        case "scout":
            # This needs to be a check only since there's a submenu
            if pass_weeks(1, dry_run=True):
                scout_menu()
        case "recruit_goblins":
            clear()
            print(colored("RECRUIT", "blue"))
            if pass_weeks(2):
                recruit(state[StateKey.COMMANDER])
        case "view_horde":
            clear()
            state[StateKey.HORDE].print_members()
        case "view_profile":
            clear()
            state[StateKey.COMMANDER].print_profile()
            print()
            show_stash()
        case "quit":
            print("Goodbye, commander.")
            sys.exit()
        case _:
            print("Please select a different option.\n")

    game_menu()


def name_menu():
    name_selection = show_name_menu()

    random_name = choice(Goblin.name_options)

    match name_selection:
        case "enter":
            name = show_name_input(random_name)
        case "random":
            name = random_name

    print(f"\nAll right. {name} it is.")

    title_selection = show_title_menu()

    state[StateKey.COMMANDER] = GoblinCommander(name, title_selection)

    clear()

    print("All right, so you will forever be known as "
          f"{state[StateKey.COMMANDER].name} the {state[StateKey.COMMANDER].adjective}.")


def new_game():
    clear()

    show_prelude()

    name_menu()

    # Generate settlements
    generated_settlement_types = choices([NomadEncampment, QuietVillage, BusyTown, BustlingCity, GleamingCastle],
                                         cum_weights=[15, 40, 85, 95, 100],
                                         k=randint(15, 25))
    state[StateKey.SETTLEMENTS] = [settlement_type() for settlement_type in generated_settlement_types]

    # Generate horde
    state[StateKey.HORDE] = Horde.generate_horde(commander=state[StateKey.COMMANDER])
    # Subtract 1 from the count here to ignore the commander
    print(f"\nYou have attracted a stunning horde of {len(state[StateKey.HORDE].members) - 1} goblin(s).")
    horde_upkeep = state[StateKey.HORDE].get_upkeep()
    print(f"They will require {horde_upkeep.food} food and {horde_upkeep.gold} gold each week to stay happy.\n")

    # Add stash
    state[StateKey.STASH] = Stash(food=500, gold=100)

    # Set in-game week
    state[StateKey.WEEK] = 1

    game_menu()


def main_menu():
    selection = show_main_menu()
    # TODO: add save/load system

    match selection:
        case "NEW":
            new_game()
        case _:
            print("Please select a different option.\n")
            main_menu()


def main():
    clear()
    print_title_figure("Goblin Commander")

    main_menu()


if __name__ == "__main__":
    main()
