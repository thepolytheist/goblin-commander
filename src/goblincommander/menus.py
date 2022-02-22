import sys

from inquirer import List, prompt, Text
from tabulate import tabulate

from goblincommander.creatures import GoblinCommander
from goblincommander.settlements import Settlement

MAIN_MENU_SELECTION = [
    List("main_menu_selection",
         message="What would you like to do, commander?",
         choices=[("NEW GAME", "NEW"),
                  # TODO: Add settings
                  # "OPTIONS",
                  "QUIT"],
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
                  ("Explore area for more settlements (1 week)", "explore"),
                  ("Recruit goblins (2 weeks)", "recruit_goblins"),
                  ("Recruit ogres (2 weeks)", "recruit_ogres"),
                  ("Recruit orcs (4 weeks)", "recruit_orcs"),
                  ("Cull horde", "cull_horde"),
                  ("View horde", "view_horde"),
                  ("View your profile", "view_profile"),
                  ("Return to main menu", "quit")],
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


def show_main_menu(*, new_game_fn, quit_fn):
    selection = process_single_selection_menu(MAIN_MENU_SELECTION)
    match selection:
        case "NEW":
            new_game_fn()
        case "QUIT":
            quit_fn()
        case _:
            print("Please select a different option.\n")
            show_main_menu(new_game_fn=new_game_fn, quit_fn=quit_fn)


def show_name_menu(*, random_name: str) -> str:
    selection = process_single_selection_menu(NAME_MENU_SELECTION)
    name = random_name
    match selection:
        case "enter":
            name = show_name_input(random_name)

    return name


def show_name_input(random_name: str):
    return prompt([Text("name_input",
                        "Why don't you write your name down here so I don't forget again?",
                        random_name)])["name_input"]


def show_title_menu():
    return process_single_selection_menu(TITLE_MENU_SELECTION)


def show_game_menu(*, raid_fn, scout_fn, recruit_goblins_fn, recruit_ogres_fn, recruit_orcs_fn, explore_fn,
                   cull_horde_fn, view_horde_fn, view_profile_fn, quit_fn):
    selection = process_single_selection_menu(GAME_MENU_SELECTION)
    match selection:
        case "raid":
            raid_fn()
        case "scout":
            scout_fn()
        case "recruit_goblins":
            recruit_goblins_fn()
        case "recruit_ogres":
            recruit_ogres_fn()
        case "recruit_orcs":
            recruit_orcs_fn()
        case "explore":
            explore_fn()
        case "cull_horde":
            cull_horde_fn()
        case "view_horde":
            view_horde_fn()
        case "view_profile":
            view_profile_fn()
        case "quit":
            quit_fn()
        case _:
            print("Please select a different option.\n")


def get_raid_menu_description(settlement: Settlement) -> tuple[str, str, str]:
    description = f"{settlement.name}, a {settlement.settlement_type}"
    guards = f"Guarded by {len(settlement.militia.members)} men"

    if settlement.scouted:
        report = f"(Beef: {settlement.militia.get_total_beef()}," \
                 f" reward: {settlement.reward.food} food, {settlement.reward.gold} gold)"
    else:
        report = f"(expected Beef: {settlement.expected_beef}, " \
                 f"expected reward: {settlement.expected_food} food, {settlement.expected_gold} gold)"

    # TODO: Re-style menu
    return description, guards, report


def show_raid_menu(current_beef: int, settlements: list[Settlement], *, raid_fn):
    print(f"Your horde currently has {current_beef} Beef.")
    valid_settlements = [s for s in settlements if not s.defeated and s.militia]
    valid_settlements.sort(key=lambda s: s.expected_beef, reverse=True)
    descriptions = tabulate([get_raid_menu_description(s) for s in valid_settlements]).splitlines()[1:]
    choices = list(zip(descriptions, valid_settlements))
    choices.append("Back")
    selection = process_single_selection_menu([List("raid_menu_selection",
                                                    message="Which settlement would you like to raid?",
                                                    choices=choices,
                                                    carousel=True)])
    match selection:
        case Settlement() as s:
            raid_fn(s)


def show_surrender_menu(settlement: Settlement, commander: GoblinCommander):
    print("As your horde approaches, a lone herald stands before the settlement's defenses.\n\n\"Greetings, Great "
          f"{commander.name} the {commander.adjective}. We, the humble people of {settlement.name}, acknowledge "
          "the ferocity of your horde and the wisdom of your leadership. We have food and gold for you to "
          "plunder, but we also have our lives. Let us prevent bloodshed this day that we may instead spill "
          f"blood in your service. What say you, mighty {commander.name}?\"\n\nThe herald appears to be offering the "
          "town's militia in place of their coffers.")
    choices = [("Bring them into the fold, then. Let's turn them loose on their own kind. (absorb militia)", "accept"),
               ("We have no use for their lives. (continue raid)", "raid")]
    return process_single_selection_menu([List("surrender_menu_selection",
                                               message="What do you think, commander?",
                                               choices=choices,
                                               carousel=True)]) == "accept"


def show_scout_menu(current_beef: int, settlements: list[Settlement], *, scout_fn):
    print(f"Your horde currently has {current_beef} Beef.")
    valid_settlements = [s for s in settlements if not s.defeated and s.militia and not s.scouted]
    valid_settlements.sort(key=lambda s: s.expected_beef, reverse=True)
    descriptions = tabulate([get_raid_menu_description(s) for s in valid_settlements]).splitlines()[1:]
    choices = list(zip(descriptions, valid_settlements))
    choices.append("Back")
    selection = process_single_selection_menu([List("scout_menu_selection",
                                                    message="Which settlement would you like to scout?",
                                                    choices=choices,
                                                    carousel=True)])
    match selection:
        case Settlement() as s:
            scout_fn(s)
