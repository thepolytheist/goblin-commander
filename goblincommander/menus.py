import sys

from inquirer import List, prompt

from settlements import Settlement

MAIN_MENU_SELECTION = [
    List("main_menu_selection",
         message="Welcome",
         choices=["NEW",
                  "OPTIONS"],
         carousel=True)
]

GAME_MENU_SELECTION = [
    List("game_menu_selection",
         message="What would you like to do, commander?",
         choices=["View horde",
                  "Raid nearby settlement (1 week)",
                  "Recruit for the horde (2 weeks)",
                  "Quit"],
         carousel=True)
]

# TODO: Remove this?
RAID_MENU_SELECTION = []


def process_single_selection_menu(selection_config: list[List]):
    response = prompt(selection_config)
    if response is None:
        print("Goodbye, commander.")
        sys.exit()
    return response[selection_config[0].name]


def show_main_menu():
    return process_single_selection_menu(MAIN_MENU_SELECTION)


def show_game_menu():
    return process_single_selection_menu(GAME_MENU_SELECTION)


def show_raid_menu(settlements: list[Settlement]):
    choices = list((s.get_raid_menu_description(), s) for s in settlements if not s.defeated and s.militia)
    choices.append("Back")
    return process_single_selection_menu([List("raid_menu_selection",
                                               message="Which settlement would you like to raid?",
                                               choices=choices,
                                               carousel=True)])
