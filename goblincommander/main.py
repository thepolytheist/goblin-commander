import json
import os
import sys
from enum import Enum
from random import randint, choices
from typing import Any

from goblin import Goblin
from stash import Stash
from horde import Horde
from intro import print_title_figure, show_prelude
from menus import show_game_menu, show_main_menu, show_raid_menu
from settlements import Settlement, NomadEncampment, QuietVillage, BusyTown, BustlingCity, GleamingCastle


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
              f"and {horde_upkeep.food * n} to stay happy.")
    return True


def raid_menu():
    selection = show_raid_menu(state[StateKey.SETTLEMENTS])

    match selection:
        case Settlement() as s:
            pass_weeks(1)
            print(f"You've chosen to raid {s.name}.")
            s = state[StateKey.HORDE].raid(s)
            if s.defeated:
                print(f"Your successful raid added {s.reward['food']} food and {s.reward['gold']} gold to the stash.")
                state[StateKey.STASH].food += s.reward["food"]
                state[StateKey.STASH].gold += s.reward["gold"]


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
    state[StateKey.STASH] = Stash()

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
