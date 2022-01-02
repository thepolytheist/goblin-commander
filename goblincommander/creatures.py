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


class Ogre(Creature):
    """Model representing an individual Ogre in the horde."""

    # Ogre stat configuration
    MINIMUM_BEEF = 6
    MAXIMUM_BEEF = 10
    MINIMUM_CUNNING = 1
    MAXIMUM_CUNNING = 3
    MINIMUM_QUICKNESS = 2
    MAXIMUM_QUICKNESS = 4

    FOOD_UPKEEP = 12
    GOLD_UPKEEP = 4

    # Load Ogre descriptive data
    with open(os.path.join(sys.path[0], 'ogre_data.json')) as f:
        ogre_data = json.loads(f.read())
        name_options = ogre_data["name_options"]
        adjective_options = ogre_data["adjective_options"]
        del ogre_data

        # TODO: Turn this into module method
        @staticmethod
        def generate_stats():
            return {StatKey.BEEF: BeefStat(randint(Ogre.MINIMUM_BEEF, Ogre.MAXIMUM_BEEF)),
                    StatKey.CUNNING: CunningStat(randint(Ogre.MINIMUM_CUNNING, Ogre.MAXIMUM_CUNNING)),
                    StatKey.QUICKNESS: QuicknessStat(randint(Ogre.MINIMUM_QUICKNESS, Ogre.MAXIMUM_QUICKNESS)),
                    StatKey.REPUTATION: ReputationStat(.5 * randint(1, 10))}

        def __init__(self):
            if not Ogre.name_options or not Ogre.adjective_options:
                raise RuntimeError("You forgot to set Ogre data, idiot.")

            super().__init__(choice(Ogre.name_options), 
                             choice(Ogre.adjective_options), 
                             Ogre.generate_stats(), 
                             Upkeep(Ogre.FOOD_UPKEEP, Ogre.GOLD_UPKEEP))

        def describe(self) -> str:
            """Gets a basic description string of the Ogre."""
            return super().describe("ogre")
        
        
class Orc(Creature):
    """Model representing an individual Orc in the horde."""

    # Orc stat configuration
    MINIMUM_BEEF = 4
    MAXIMUM_BEEF = 7
    MINIMUM_CUNNING = 1
    MAXIMUM_CUNNING = 6
    MINIMUM_QUICKNESS = 2
    MAXIMUM_QUICKNESS = 6

    FOOD_UPKEEP = 8
    GOLD_UPKEEP = 2

    # Load Orc descriptive data
    with open(os.path.join(sys.path[0], 'orc_data.json')) as f:
        orc_data = json.loads(f.read())
        name_options = orc_data["name_options"]
        adjective_options = orc_data["adjective_options"]
        del orc_data

        # TODO: Turn this into module method
        @staticmethod
        def generate_stats():
            return {StatKey.BEEF: BeefStat(randint(Orc.MINIMUM_BEEF, Orc.MAXIMUM_BEEF)),
                    StatKey.CUNNING: CunningStat(randint(Orc.MINIMUM_CUNNING, Orc.MAXIMUM_CUNNING)),
                    StatKey.QUICKNESS: QuicknessStat(randint(Orc.MINIMUM_QUICKNESS, Orc.MAXIMUM_QUICKNESS)),
                    StatKey.REPUTATION: ReputationStat(.5 * randint(1, 10))}

        def __init__(self):
            if not Orc.name_options or not Orc.adjective_options:
                raise RuntimeError("You forgot to set Orc data, idiot.")

            super().__init__(choice(Orc.name_options), 
                             choice(Orc.adjective_options), 
                             Orc.generate_stats(), 
                             Upkeep(Orc.FOOD_UPKEEP, Orc.GOLD_UPKEEP))

        def describe(self) -> str:
            """Gets a basic description string of the Orc."""
            return super().describe("orc")