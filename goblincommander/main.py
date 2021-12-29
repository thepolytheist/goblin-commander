import json
import os
import sys
from enum import Enum
from random import randint
from typing import Any

from goblin import Goblin
from horde import Horde
from intro import print_title_figure, show_prelude
from menus import show_game_menu, show_main_menu, show_raid_menu
from settlement import Settlement


class StateKey(str, Enum):
    HORDE = "horde"
    SETTLEMENTS = "settlements"


state: dict[StateKey, Any] = {}


def raid_menu():
    selection = show_raid_menu(state[StateKey.SETTLEMENTS])

    match selection:
        case Settlement() as s:
            print(f"You've chosen to raid {s.name}.")
            s = state[StateKey.HORDE].raid(s)
            print(s)
            game_menu()
        case "Back":
            game_menu()


def game_menu():
    selection = show_game_menu()

    # Manage horde
    # Raid nearby settlement
    #     Nomads, village, town, city, castle
    match selection:
        case "View horde":
            state[StateKey.HORDE].print_members()
            game_menu()
        case "Raid nearby settlement":
            raid_menu()
        case "Quit":
            print("Goodbye, commander.")
            sys.exit()
        case _:
            print("Please select a different option.\n")
            game_menu()


def new_game():
    show_prelude()

    # Generate settlements
    state[StateKey.SETTLEMENTS] = [Settlement() for _ in range(randint(5, 10))]

    # Generate horde
    state[StateKey.HORDE] = Horde.generate_horde()
    print(f"You have attracted a stunning horde of {len(state[StateKey.HORDE].members)} goblin(s).\n")
    horde_upkeep = state[StateKey.HORDE].get_upkeep()
    print(f"They will require {horde_upkeep.food} food and {horde_upkeep.gold} gold each week to stay happy.\n")

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
