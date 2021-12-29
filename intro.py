from pyfiglet import Figlet
from termcolor import colored


def print_title_figure(text):
    """Prints the provided text as a Figlet. Disallows multiple calls."""
    # Prevent the intro from being printed multiple times
    if not print_title_figure.has_been_called:
        f = Figlet(font='slant')
        print(colored(f.renderText(text.upper()), "green"))
        print_title_figure.has_been_called = True


# Set flag to track whether the title figure has been shown
print_title_figure.has_been_called = False


def show_prelude():
    print("You are the vaunted commander of a rioting horde. Your skin is green, and your heart is cold. "
          "Lead your minions to victory.\n")
