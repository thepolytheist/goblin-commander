import os
from enum import Enum
from typing import Optional, Callable

from rich import print


class ConsoleColor(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"


def clear():
    """Pushes old content off the top of the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def styled(text: str, *, color: Optional[ConsoleColor] = None):
    if color is None:
        return text

    return f"[{color}]{text}[/{color}]"


def print_styled(text: str, color: Optional[ConsoleColor] = None, transformer: Optional[Callable[[str], str]] = None):
    if transformer is not None:
        text = transformer(text)

    print(styled(text, color=color))


def print_header(header: str, color: Optional[ConsoleColor] = None):
    if color is None:
        color = ConsoleColor.BLUE

    clear()
    print_styled(header, color, lambda s: s.upper())
