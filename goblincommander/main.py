import json
import os
import sys
from enum import Enum
from random import randint, choices
from typing import Any

from creature_groups import Horde
from creatures import Goblin
from intro import print_title_figure, show_prelude
from menus import show_game_menu, show_main_menu, show_raid_menu, show_scout_menu
from settlements import Settlement, NomadEncampment, QuietVillage, BusyTown, BustlingCity, GleamingCastle
from stash import Stash
from stats import StatKey


class StateKey(str, Enum):
    HORDE = "horde"
    SETTLEMENTS = "settlements"
    STASH = "stash"
    WEEK = "week"


state: dict[StateKey, Any] = {}


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

    print(f"Base horde strength: {horde_beef}")
    print(f"Base militia strength: {militia_beef}")

    if horde.get_stat_avg(StatKey.REPUTATION) > 4.5:
        print(f"\nThe {settlement.name} defense is losing their wits in the face of your famous might.")
        militia_cunning *= 0.7
        print(f"Adjusted horde strength: {horde_beef:.2f}")
        print(f"Adjusted militia strength: {militia_beef:.2f}")

    if horde.get_stat_avg(StatKey.QUICKNESS) > settlement.militia.get_stat_avg(StatKey.QUICKNESS):
        print(f"\nYour speedy horde got the drop on the {settlement.name} defenses! You've caught them unprepared.")
        militia_beef *= 0.9
    else:
        if settlement.scouted:
            print(f"\nThe {settlement.name} militia rallied quickly,"
                  " but your scouts found a critical flaw in their defenses. Not to worry.")
        else:
            print(f"\nUh oh. The {settlement.name} defenses rallied their forces in record time."
                  " You've got your work cut out for you.")
            horde_beef *= 0.9

    print(f"Adjusted horde strength: {horde_beef:.2f}")
    print(f"Adjusted militia strength: {militia_beef:.2f}")

    # Need to use local militia cunning to allow for modification
    if settlement.scouted or horde.get_stat_avg(StatKey.CUNNING) > militia_cunning / len(settlement.militia.members):
        if settlement.scouted:
            print(f"\nThe information from your scouts has given you the tactical edge.")
        else:
            print(f"\nThe {settlement.name} defenses don't seem too bright. Let's show them who's boss.")
        horde_beef *= 1.1
    else:
        print(f"\nHmm. These men defending {settlement.name} are smarter than we thought."
              " Best keep our heads on straight.")
        militia_beef *= 1.1

    print(f"Adjusted horde strength: {horde_beef:.2f}")
    print(f"Adjusted militia strength: {militia_beef:.2f}")
    if horde_beef > militia_beef:
        print(f"\nYour horde defeated the pitiful defenses of {settlement.name}.")
        settlement.defeated = True
        settlement.militia.members = []
        horde.bolster()
    else:
        print(f"\nYour pitiful horde was defeated by the defenses of {settlement.name}. "
              "Half of them didn't make it back.")
        horde.members = [m for i, m in enumerate(horde.members) if i % 2 == 0]
    return settlement


def raid_menu():
    print(f"Your horde currently has {state[StateKey.HORDE].get_stat_sum(StatKey.BEEF)} Beef.")
    selection = show_raid_menu(state[StateKey.SETTLEMENTS])

    match selection:
        case Settlement() as s:
            pass_weeks(1)
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
            s.scouted = True
            print(f"Your scouts have gained valuable info about {s.name}:")
            print(f"Beef: {s.militia.get_stat_sum(StatKey.BEEF)}, "
                  f"reward: {s.reward.food} food, {s.reward.gold} gold")


def recruit():
    # TODO: Base on commander reputation
    print(f"With your charisma and notoriety, you've managed to recruit more goblins.")
    state[StateKey.HORDE].bolster()


def game_menu():
    print(f"\nWeek {state[StateKey.WEEK]}")
    show_stash()
    selection = show_game_menu()

    # Manage horde
    # Raid nearby settlement
    #     Nomads, village, town, city, castle
    match selection:
        case "View horde":
            state[StateKey.HORDE].print_members()
        case "Raid nearby settlement (1 week)":
            # This needs to be a check only since there's a submenu
            if pass_weeks(1, dry_run=True):
                raid_menu()
        case "Scout nearby settlement (1 week)":
            # This needs to be a check only since there's a submenu
            if pass_weeks(1, dry_run=True):
                scout_menu()
        case "Recruit for the horde (2 weeks)":
            if pass_weeks(2):
                recruit()
        case "Quit":
            print("Goodbye, commander.")
            sys.exit()
        case _:
            print("Please select a different option.\n")

    game_menu()


def new_game():
    show_prelude()

    # Generate settlements
    generated_settlement_types = choices([NomadEncampment, QuietVillage, BusyTown, BustlingCity, GleamingCastle],
                                         cum_weights=[15, 40, 85, 95, 100],
                                         k=randint(15, 25))
    state[StateKey.SETTLEMENTS] = [settlement_type() for settlement_type in generated_settlement_types]

    # Generate horde
    state[StateKey.HORDE] = Horde.generate_horde()
    print(f"You have attracted a stunning horde of {len(state[StateKey.HORDE].members)} goblin(s).\n")
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
    with open(os.path.join(sys.path[0], 'goblin_data.json')) as f:
        goblin_data = json.loads(f.read())
        Goblin.set_name_options(goblin_data["name_options"])
        Goblin.set_adjective_options(goblin_data["adjective_options"])

    # TODO: Load data for other creatures

    print_title_figure("Goblin Commander")

    main_menu()


if __name__ == "__main__":
    main()
