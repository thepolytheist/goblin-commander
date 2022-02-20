import random
import sys
from enum import Enum
from random import randint, choices, choice, sample
from typing import Any, Type

from goblincommander import console, creature_groups
from goblincommander.creature_groups import Horde
from goblincommander.creatures import Goblin, GoblinCommander, Ogre, Orc, Creature
from goblincommander.menus import show_game_menu, show_main_menu, show_raid_menu, show_scout_menu, show_name_menu, \
    show_name_input, show_title_menu, show_surrender_menu
from goblincommander.printers import print_creature_group, print_title_figure, print_victory_figure
from goblincommander.settlements import Settlement, NomadEncampment, QuietVillage, BusyTown, BustlingCity, \
    GleamingCastle
from goblincommander.stash import Stash


class StateKey(str, Enum):
    COMMANDER = "commander"
    HORDE = "horde"
    SETTLEMENTS = "settlements"
    STASH = "stash"
    WEEK = "week"


state: dict[StateKey, Any] = {}


def show_stash():
    horde_upkeep = state[StateKey.HORDE].get_upkeep()
    stash = state[StateKey.STASH]
    print(f"You have {stash.food} food and {stash.gold} gold remaining in your stash.")
    remaining_weeks = min(stash.food // horde_upkeep.food, stash.gold // horde_upkeep.gold)
    print(f"This is enough to keep your horde happy for {remaining_weeks} week(s).")


def update_settlements(week_number: int):
    active_settlements = list(filter(lambda s: not s.defeated, state[StateKey.SETTLEMENTS]))
    needs_settlements = len(active_settlements) == 0
    if week_number < 5:
        if needs_settlements:
            state[StateKey.SETTLEMENTS].extend([NomadEncampment(), QuietVillage(), QuietVillage()])
        elif len(active_settlements) < week_number and random.random() > 0.8:
            state[StateKey.SETTLEMENTS].append(random.choice([NomadEncampment(), QuietVillage()]))
    elif week_number < 10:
        if needs_settlements:
            state[StateKey.SETTLEMENTS].extend([QuietVillage(), QuietVillage(), BusyTown()])
        elif len(active_settlements) < week_number and random.random() > 0.8:
            state[StateKey.SETTLEMENTS].append(random.choice([QuietVillage(), BusyTown(), BustlingCity()]))
    elif week_number < 15:
        if needs_settlements:
            state[StateKey.SETTLEMENTS].extend([BusyTown(), BusyTown(), BustlingCity()])
        elif len(active_settlements) < week_number and random.random() > 0.8:
            state[StateKey.SETTLEMENTS].append(
                random.choice([QuietVillage(), BusyTown(), BustlingCity(), GleamingCastle()]))
    else:
        if needs_settlements:
            state[StateKey.SETTLEMENTS].extend([BusyTown(), BustlingCity(), BustlingCity()])
        elif len(active_settlements) < week_number and random.random() > 0.8:
            state[StateKey.SETTLEMENTS].append(random.choice([BustlingCity(), GleamingCastle()]))


def pass_weeks(n: int, dry_run=False) -> bool:
    horde_upkeep = state[StateKey.HORDE].get_upkeep()
    stash = state[StateKey.STASH]

    if horde_upkeep.gold * n > stash.gold or horde_upkeep.food * n > stash.food:
        print("You will need a bigger stash for that. "
              f"Maintaining your horde for {n} week(s) will require {horde_upkeep.food * n} food "
              f"and {horde_upkeep.gold * n} gold.\n")
        show_stash()
        return False

    if not dry_run:
        stash.gold -= horde_upkeep.gold * n
        stash.food -= horde_upkeep.food * n
        state[StateKey.WEEK] += n
        print(f"{n} week(s) have passed. In this time, your horde has required {horde_upkeep.gold * n} gold "
              f"and {horde_upkeep.food * n} food to stay happy.")
    return True


def quit_game():
    print("Goodbye, commander.")
    sys.exit()


def check_for_victory():
    # If not all settlements are defeated or there are no castles, no victory yet
    if any(map(lambda s: not s.defeated, state[StateKey.SETTLEMENTS])) or all(
            map(lambda s: not isinstance(s, GleamingCastle), state[StateKey.SETTLEMENTS])):
        return

    commander = state[StateKey.COMMANDER]
    stash = state[StateKey.STASH]
    print_victory_figure()
    print("Congratulations, commander!")
    print(f"The horde of {commander.name} the {commander.adjective} has swarmed over the land, "
          f"conquering {len(state[StateKey.SETTLEMENTS])} settlements in {state[StateKey.WEEK]} weeks.")
    print(f"\nYour horde had {stash.food} food and {stash.gold} gold remaining.")
    main_menu()


def add_members_to_horde(horde: Horde, creature_type: Type[Creature], minimum: int, maximum: int) -> None:
    """
    Adds a number of creatures to the horde between the minimum and maximum values of the creature type provided.
    """
    num_new_creatures = randint(minimum, maximum)
    if num_new_creatures > 0:
        name = creature_type.__name__.lower()
        print(f"\nYou've attracted {num_new_creatures} new {name}s!")
        # noinspection PyArgumentList
        new_creatures = [creature_type() for _ in range(num_new_creatures)]
        new_reputation = horde.get_avg_reputation() * 0.9
        for creature in new_creatures:
            creature.stats.reputation.value = max(creature.stats.reputation.value, new_reputation)
        horde.bolster(new_creatures)
        print(f"Your horde now boasts {len(horde.members)} in its ranks!")
    else:
        print("\nSeems no one showed up today. What a shame.")


def cull_horde(horde: Horde, creature_types: list[Type[Creature]], minimum: int, maximum: int):
    """
    Removes a number of creatures between the minimum and maximum values based
    on the candidate creature types provided.
    """
    num_to_cull = min(randint(minimum, maximum), len(horde.members))
    candidate_creatures = [m for m in horde.members if type(m) in creature_types and not m.is_commander]
    if num_to_cull <= 0 or len(candidate_creatures) == 0:
        print("\nLooks like everyone survived today.")
    else:
        num_to_cull = min(len(candidate_creatures), num_to_cull)
        print(f"\n{num_to_cull} of your horde didn't make it back alive.")
        horde.cull(sample(candidate_creatures, k=num_to_cull))


def raid(horde: Horde, settlement: Settlement) -> None:
    if settlement.defeated or not settlement.militia:
        raise ValueError("Raid target is not a valid settlement for raiding.")

    # TODO: Refactor this process for testability

    horde_beef = horde.get_total_beef()

    militia_beef = settlement.militia.get_total_beef()
    militia_cunning = settlement.militia.get_total_cunning()

    print(settlement.description)

    print(f"\nBase horde Beef: {horde_beef:.2f}")
    print(f"Base militia Beef: {militia_beef:.2f}\n")

    if horde.get_avg_reputation() > 4.5:
        if settlement.militia.get_avg_cunning() > 7.0:
            surrender_choice = show_surrender_menu(settlement, state[StateKey.COMMANDER])
            match surrender_choice:
                case "accept":
                    console.print_header("victory", console.ConsoleColor.GREEN)
                    print(f"The {len(settlement.militia.members)} men of {settlement.name}'s "
                          "militia have joined your horde!")
                    horde.bolster(settlement.militia.members)
                    settlement.defeated = True
                    settlement.scouted = True
                    settlement.militia.members = []
                    for creature in state[StateKey.HORDE].members:
                        creature.stats.reputation.value = min(creature.stats.reputation.value + settlement.reputation,
                                                              5.0)
                    check_for_victory()
                    return

        print(f"[REP] The {settlement.name} defense is losing their wits in the face of your famous might. ", end="")
        console.print_styled(f"(-{militia_cunning * 0.3:.2f} militia Cunning)", console.ConsoleColor.GREEN)
        militia_cunning *= 0.7

    if horde.get_avg_quickness() > settlement.militia.get_avg_quickness():
        print(
            f"[QCK] Your speedy horde got the drop on the {settlement.name} defenses! You've caught them unprepared. ",
            end="")
        console.print_styled(f"(-{militia_beef * 0.1:.2f} militia Beef)", console.ConsoleColor.GREEN)
        militia_beef *= 0.9
    else:
        if settlement.scouted:
            print(f"[QCK] The {settlement.name} militia rallied quickly,"
                  " but your scouts found a critical flaw in their defenses. Not to worry. (No change)")
        else:
            print(f"[QCK] Uh oh. The {settlement.name} defenses rallied their forces in record time."
                  f" You've got your work cut out for you. ", end="")
            console.print_styled(f"(-{horde_beef * 0.1:.2f} horde Beef)", console.ConsoleColor.RED)
            horde_beef *= 0.9

    # Need to use local militia cunning to allow for modification
    if settlement.scouted or horde.get_avg_cunning() > militia_cunning / len(settlement.militia.members):
        if settlement.scouted:
            print(f"[CUN] The information from your scouts has given you the tactical edge. ", end="")
        else:
            print(f"[CUN] The {settlement.name} defenses don't seem too bright. Let's show them who's boss. ", end="")
        console.print_styled(f"(+{horde_beef * 0.1:.2f} horde Beef)", console.ConsoleColor.GREEN)
        horde_beef *= 1.1
    else:
        print(f"[CUN] Hmm. These men defending {settlement.name} are smarter than we thought."
              f" Best keep our heads on straight. ", end="")
        console.print_styled(f"(+{militia_beef * 0.1:.2f} militia Beef)", console.ConsoleColor.RED)
        militia_beef *= 1.1

    print(f"\nAdjusted horde Beef: {horde_beef:.2f}")
    print(f"Adjusted militia Beef: {militia_beef:.2f}\n")
    if horde_beef > militia_beef:
        console.print_styled("VICTORY", console.ConsoleColor.GREEN)
        print(f"Your horde defeated the pitiful defenses of {settlement.name}.")
        settlement.defeated = True
        settlement.militia.members = []
        add_members_to_horde(horde, Goblin, 1, 3)
        print(f"Your successful raid added {settlement.reward.food} food "
              f"and {settlement.reward.gold} gold to the stash.")
        state[StateKey.STASH] += settlement.reward
        for creature in state[StateKey.HORDE].members:
            creature.stats.reputation.value = min(creature.stats.reputation.value + settlement.reputation, 5.0)
        check_for_victory()
    else:
        console.print_styled("DEFEAT", console.ConsoleColor.RED)
        print(f"Your pitiful horde was defeated by the defenses of {settlement.name}. "
              "Some of them didn't make it back.")
        cull_horde(horde, [Goblin, Ogre, Orc], 3, 5)
        for creature in state[StateKey.HORDE].members:
            creature.stats.reputation.value = max(creature.stats.reputation.value - settlement.reputation,
                                                  0.0)
    settlement.scouted = True


def raid_menu():
    print(f"Your horde currently has {state[StateKey.HORDE].get_total_beef()} Beef.")
    selection = show_raid_menu(state[StateKey.SETTLEMENTS])

    match selection:
        case Settlement() as s:
            pass_weeks(1, dry_run=True)
            console.print_header("raid")
            print(f"You've chosen to raid {s.name}.")
            raid(state[StateKey.HORDE], s)
            pass_weeks(1)
            update_settlements(state[StateKey.WEEK])


def scout_menu():
    print(f"Your horde currently has {state[StateKey.HORDE].get_total_beef()} Beef.")
    selection = show_scout_menu(state[StateKey.SETTLEMENTS])

    match selection:
        case Settlement() as s:
            pass_weeks(1)
            console.print_header("scout")
            s.scouted = True
            print(f"Your scouts have gained valuable info about {s.name}:")
            print(f"Beef: {s.militia.get_total_beef()}, "
                  f"reward: {s.reward.food} food, {s.reward.gold} gold")


def recruit_goblins(commander: GoblinCommander, horde: Horde):
    reputation = commander.stats.reputation.value
    print()
    if reputation == 5.0:
        print(f"No goblin is more feared or admired than {commander.name} the {commander.adjective}. "
              "Other creatures are running to join your famous horde.")
        add_members_to_horde(horde, Goblin, 4, 5)
    elif reputation > 4.0:
        print(f"The name {commander.name} is known far and wide. "
              "With your charisma and notoriety, you've managed to recruit more creatures.")
        add_members_to_horde(horde, Goblin, 3, 4)
    elif reputation > 3.0:
        print(f"Creatures in the area are beginning to recognize the name {commander.name}. "
              "They don't need a lot of convincing to come fight for you.")
        add_members_to_horde(horde, Goblin, 2, 4)
    elif reputation > 2.0:
        print(f"No one's heard of {commander.name} the {commander.adjective}, "
              "but there are still some creatures looking for work.")
        add_members_to_horde(horde, Goblin, 1, 3)
    elif reputation > 1.0:
        print(f"{commander.name} the {commander.adjective} is known more for struggling and losing than anything else."
              " Regardless, you might be able to convince some creatures to follow you.")
        add_members_to_horde(horde, Goblin, 1, 2)
    else:
        # reputation < 1.0
        print(f"Good luck finding anyone who wants to join the unlucky horde of {commander.name} the Fallible.")
        add_members_to_horde(horde, Goblin, 0, 1)


def recruit_ogres(horde: Horde):
    if horde.get_avg_quickness() > 6:
        print("Your goblins reported communication difficulties, "
              "but they convinced some ogres to return with them regardless.")
    else:
        print("Your goblins brought back ogres for the horde, but not without facing danger.")
        cull_horde(horde, [Goblin], 3, 5)
    add_members_to_horde(horde, Ogre, 2, 3)


def recruit_orcs(horde: Horde):
    print("It took some time, but you've managed to convince an orc raiding party to join your horde.")
    add_members_to_horde(horde, Orc, 4, 6)


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
            console.print_header("recruit")
            if pass_weeks(2):
                recruit_goblins(state[StateKey.COMMANDER], state[StateKey.HORDE])
        case "recruit_ogres":
            console.print_header("recruit")
            if pass_weeks(2):
                recruit_ogres(state[StateKey.HORDE])
        case "recruit_orcs":
            console.print_header("recruit")
            if pass_weeks(4):
                recruit_orcs(state[StateKey.HORDE])
        case "view_horde":
            console.clear()
            print_creature_group(state[StateKey.HORDE])
        case "view_profile":
            console.clear()
            state[StateKey.COMMANDER].print_profile()
            print()
            show_stash()
        case "quit":
            main_menu()
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

    console.clear()

    print("All right, so you will forever be known as "
          f"{state[StateKey.COMMANDER].name} the {state[StateKey.COMMANDER].adjective}.")


def new_game():
    console.clear()

    print("You are the vaunted commander of a rioting horde. Your skin is green, and your heart is cold. "
          "Lead your minions to victory.\n")

    name_menu()

    # Generate settlements
    generated_settlement_types = choices([NomadEncampment, QuietVillage, BusyTown],
                                         cum_weights=[55, 90, 100],
                                         k=randint(5, 10))
    state[StateKey.SETTLEMENTS] = [settlement_type() for settlement_type in generated_settlement_types]

    # Generate horde
    state[StateKey.HORDE] = creature_groups.generate_horde(commander=state[StateKey.COMMANDER])
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
        case "QUIT":
            quit_game()
        case _:
            print("Please select a different option.\n")
            main_menu()


def main():
    console.clear()
    print_title_figure("Goblin Commander")

    main_menu()


if __name__ == "__main__":
    main()
