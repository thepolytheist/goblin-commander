import sys

from inquirer import List, prompt, Text

from settlements import Settlement

MAIN_MENU_SELECTION = [
    List("main_menu_selection",
         message="Welcome",
         choices=["NEW",
                  "OPTIONS"],
         carousel=True)
]

NAME_MENU_SELECTION = [
    List("name_menu_select",
         message="...That said, what's your name again? Should I just come up with something?",
         choices=[("I already have a name! It's... (enter name)", "enter"),
                  ("Why don't you tell me what you want to call me? (random name)", "random")])
]

TITLE_MENU_SELECTION = [
    List("title_menu_select",
         message="And what would you say you're known for?",
         choices=[("I could break a man's skull with my pinky finger. (+5 Beef)", "Skullcracker"),
                  ("Ain't no defenses that are gonna outwit me. (+5 Cunning)", "Brainy"),
                  ("Once I beat my own grandpa in a race to get some soup. (+5 Quickness)", "Swift"),
                  ("I'm known for pulling out teeth when people ask me too many question. (+2.0 Reputation)",
                   "Notorious")])
]

GAME_MENU_SELECTION = [
    List("game_menu_selection",
         message="What would you like to do, commander?",
         choices=[("Raid nearby settlement (1 week)", "raid"),
                  ("Scout nearby settlement (1 week)", "scout"),
                  ("Recruit goblins (2 weeks)", "recruit_goblins"),
                  ("Recruit ogres (2 weeks)", "recruit_ogres"),
                  ("Recruit orcs (4 weeks)", "recruit_orcs"),
                  ("View horde", "view_horde"),
                  ("View your profile", "view_profile"),
                  ("Quit", "quit")],
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


def show_name_menu():
    return process_single_selection_menu(NAME_MENU_SELECTION)


def show_name_input(random_name: str):
    return prompt([Text("name_input",
                        "Why don't you write your name down here so I don't forget again?",
                        random_name)])["name_input"]


def show_title_menu():
    return process_single_selection_menu(TITLE_MENU_SELECTION)


def show_game_menu():
    return process_single_selection_menu(GAME_MENU_SELECTION)


def show_raid_menu(settlements: list[Settlement]):
    choices = list((s.get_raid_menu_description(), s) for s in settlements if not s.defeated and s.militia)
    choices.append("Back")
    return process_single_selection_menu([List("raid_menu_selection",
                                               message="Which settlement would you like to raid?",
                                               choices=choices,
                                               carousel=True)])


def show_scout_menu(settlements: list[Settlement]):
    choices = list((s.get_raid_menu_description(), s) for s in settlements
                   if not s.defeated and s.militia and not s.scouted)
    choices.append("Back")
    return process_single_selection_menu([List("scout_menu_selection",
                                               message="Which settlement would you like to scout?",
                                               choices=choices,
                                               carousel=True)])
