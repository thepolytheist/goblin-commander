from pyfiglet import Figlet
from tabulate import tabulate

from goblincommander import console
from goblincommander.creature_groups import CreatureGroup
from goblincommander.creatures import GoblinCommander


def print_title_figure(text):
    """Prints the provided text as a Figlet. Disallows multiple calls."""
    # Prevent the intro from being printed multiple times
    if not print_title_figure.has_been_called:
        f = Figlet(font='slant')
        console.print_styled(text, console.ConsoleColor.GREEN, lambda s: f.renderText(s.upper()))
        print_title_figure.has_been_called = True


# Set flag to track whether the title figure has been shown
print_title_figure.has_been_called = False


def print_victory_figure():
    """Prints "Victory" as a Figlet."""
    f = Figlet(font='slant')
    console.print_styled("Victory", console.ConsoleColor.GREEN, lambda s: f.renderText(s))


def print_creature_group(group: CreatureGroup) -> None:
    row_data = [[creature.name, type(creature).__name__, creature.adjective,
                 str(creature.stats.beef.value),
                 str(creature.stats.cunning.value),
                 str(creature.stats.quickness.value),
                 f"{creature.stats.reputation.value:3.2f}"] for creature in group.members
                if not creature.is_commander]
    print(tabulate(row_data,
                   headers=["Name", "Type", "Adjective", "Beef", "Cunning", "Quickness", "Reputation"],
                   floatfmt=("", "", "", ".0f", ".0f", ".0f", "3.2f")))
    print()
    print(tabulate([["Averages",
                     str(group.get_avg_beef()),
                     str(group.get_avg_cunning()),
                     str(group.get_avg_quickness()),
                     str(group.get_avg_reputation())]],
                   headers=["", "Beef", "Cunning", "Quickness", "Reputation"],
                   tablefmt="plain",
                   floatfmt="3.2f"))
    print("\n*Averages include your stats")


def print_profile(commander: GoblinCommander):
    print(tabulate([[commander.name, commander.adjective,
                     str(commander.stats.beef.value),
                     str(commander.stats.cunning.value),
                     str(commander.stats.quickness.value),
                     str(commander.stats.reputation.value)]],
                   headers=["Name", "Title", "Beef", "Cunning", "Quickness", "Reputation"],
                   floatfmt=("", "", "", "", "", "3.2f")))
