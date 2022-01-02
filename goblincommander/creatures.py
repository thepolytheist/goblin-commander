import json
import os
import sys
from random import choice, randint
from typing import Optional

from tabulate import tabulate

from stats import StatKey, Stat, BeefStat, CunningStat, QuicknessStat, ReputationStat
from upkeep import Upkeep


class Creature:
    """Base class representing any creature in a horde"""

    def __init__(self, name: str, adjective: str, stats: dict[StatKey, Stat], upkeep: Upkeep, is_commander=False):
        self.name = name
        self.adjective = adjective
        self.stats = stats
        self.upkeep = upkeep
        self.is_commander = is_commander

    def describe(self, creature_type: str = "creature") -> str:
        """Gets a basic description string of the creature."""
        return f'A {self.adjective} {creature_type} named {self.name}.'

    def stats_string(self, multiline=True) -> str:
        """Gets a display string of the creature's stats for inline or multiline block printing."""
        stats_list = list(self.stats.values())
        if multiline:
            return '\t'.join([s.short_name for s in stats_list]) + '\n' + \
                   '\t'.join([str(s.value) for s in stats_list])
        return ', '.join([f'{s.short_name}: {s.value}' for s in stats_list])

    def __str__(self):
        return f'{self.describe()}\n{self.stats_string()}'


class Goblin(Creature):
    """Model representing an individual Goblin in the horde"""

    # Goblin stat configuration
    MINIMUM_BEEF = 1
    MAXIMUM_BEEF = 4
    MINIMUM_CUNNING = 2
    MAXIMUM_CUNNING = 10
    MINIMUM_QUICKNESS = 2
    MAXIMUM_QUICKNESS = 7

    FOOD_UPKEEP = 5
    GOLD_UPKEEP = 1

    # Load Goblin descriptive data
    with open(os.path.join(sys.path[0], 'goblin_data.json')) as f:
        goblin_data = json.loads(f.read())
        name_options = goblin_data["name_options"]
        adjective_options = goblin_data["adjective_options"]
        del goblin_data

    # TODO: Turn this into module method
    @staticmethod
    def generate_stats():
        return {StatKey.BEEF: BeefStat(randint(Goblin.MINIMUM_BEEF, Goblin.MAXIMUM_BEEF)),
                StatKey.CUNNING: CunningStat(randint(Goblin.MINIMUM_CUNNING, Goblin.MAXIMUM_CUNNING)),
                StatKey.QUICKNESS: QuicknessStat(randint(Goblin.MINIMUM_QUICKNESS, Goblin.MAXIMUM_QUICKNESS)),
                StatKey.REPUTATION: ReputationStat(.5 * randint(1, 10))}

    def __init__(self, name: Optional[str] = None,
                 adjective: Optional[str] = None,
                 stats: Optional[dict] = None,
                 upkeep: Optional[Upkeep] = None,
                 is_commander=False):
        if not Goblin.name_options or not Goblin.adjective_options:
            raise RuntimeError("You forgot to set Goblin data, idiot.")

        if not name:
            name = choice(Goblin.name_options)

        if not adjective:
            adjective = choice(Goblin.adjective_options)

        if not stats:
            stats = Goblin.generate_stats()

        if not upkeep:
            upkeep = Upkeep(Goblin.FOOD_UPKEEP, Goblin.GOLD_UPKEEP)

        super().__init__(name, adjective, stats, upkeep, is_commander)

    def describe(self) -> str:
        """Gets a basic description string of the Goblin."""
        return super().describe("goblin")


class GoblinCommander(Goblin):

    def __init__(self, name: str, title: str):
        stats = {
            StatKey.BEEF: BeefStat(3),
            StatKey.CUNNING: CunningStat(8),
            StatKey.QUICKNESS: QuicknessStat(5),
            StatKey.REPUTATION: ReputationStat(3.0)
        }

        match title:
            case "Skullcracker":
                stats[StatKey.BEEF].value += 5
            case "Brainy":
                stats[StatKey.CUNNING].value += 5
            case "Swift":
                stats[StatKey.QUICKNESS].value += 5
            case "Notorious":
                stats[StatKey.REPUTATION].value += 2.0

        super().__init__(name, title, stats, Upkeep(0, 0), True)

    def print_profile(self):
        print(tabulate([[self.name, self.adjective,
                         str(self.stats[StatKey.BEEF].value),
                         str(self.stats[StatKey.CUNNING].value),
                         str(self.stats[StatKey.QUICKNESS].value),
                         f"{self.stats[StatKey.REPUTATION].value:.2f}"]],
                       headers=["Name", "Title", "Beef", "Cunning", "Quickness", "Reputation"]))


class Human(Creature):
    """Model representing an individual Human protecting a settlement."""

    # Human stat configuration
    MINIMUM_BEEF = 1
    MAXIMUM_BEEF = 6
    MINIMUM_CUNNING = 3
    MAXIMUM_CUNNING = 10
    MINIMUM_QUICKNESS = 1
    MAXIMUM_QUICKNESS = 6

    FOOD_UPKEEP = 10
    GOLD_UPKEEP = 4

    # Human descriptive data
    name_options = ["Paul", "Harold", "Jimbo", "Willy", "Mark"]
    adjective_options = ["hairy", "stringy", "bold", "loud", "smelly", "pretty"]

    @staticmethod
    def generate_stats():
        return {StatKey.BEEF: BeefStat(randint(Human.MINIMUM_BEEF, Human.MAXIMUM_BEEF)),
                StatKey.CUNNING: CunningStat(randint(Human.MINIMUM_CUNNING, Human.MAXIMUM_CUNNING)),
                StatKey.QUICKNESS: QuicknessStat(randint(Human.MINIMUM_QUICKNESS, Human.MAXIMUM_QUICKNESS)),
                StatKey.REPUTATION: ReputationStat(.5 * randint(1, 10))}

    def __init__(self):
        if not Human.name_options or not Human.adjective_options:
            raise RuntimeError("You forgot to set the Human data, idiot.")

        super().__init__(choice(Human.name_options),
                         choice(Human.adjective_options),
                         Human.generate_stats(),
                         Upkeep(Human.FOOD_UPKEEP, Human.GOLD_UPKEEP))

    def describe(self) -> str:
        """Gets a basic description string of the Human."""
        return super().describe("human")
