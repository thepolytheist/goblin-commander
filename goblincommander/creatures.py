from random import choice, randint

from stats import StatKey, Stat, BeefStat, CunningStat, QuicknessStat, ReputationStat
from upkeep import Upkeep


class Creature:
    """Base class representing any creature in a horde"""

    def __init__(self, name: str, adjective: str, stats: dict[StatKey, Stat], upkeep: Upkeep):
        self.name = name
        self.adjective = adjective
        self.stats = stats
        self.upkeep = upkeep

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

    # Goblin descriptive data
    name_options = []
    adjective_options = []

    @staticmethod
    def set_name_options(names):
        Goblin.name_options = names

    @staticmethod
    def set_adjective_options(adjectives):
        Goblin.adjective_options = adjectives

    @staticmethod
    def generate_stats():
        return {StatKey.BEEF: BeefStat(randint(Goblin.MINIMUM_BEEF, Goblin.MAXIMUM_BEEF)),
                StatKey.CUNNING: CunningStat(randint(Goblin.MINIMUM_CUNNING, Goblin.MAXIMUM_CUNNING)),
                StatKey.QUICKNESS: QuicknessStat(randint(Goblin.MINIMUM_QUICKNESS, Goblin.MAXIMUM_QUICKNESS)),
                StatKey.REPUTATION: ReputationStat(.5 * randint(1, 10))}

    def __init__(self):
        if not Goblin.name_options or not Goblin.adjective_options:
            raise RuntimeError("You forgot to set Goblin data, idiot.")

        super().__init__(choice(Goblin.name_options),
                         choice(Goblin.adjective_options),
                         Goblin.generate_stats(),
                         Upkeep(Goblin.FOOD_UPKEEP, Goblin.GOLD_UPKEEP))

    def describe(self) -> str:
        """Gets a basic description string of the Goblin."""
        return super().describe("goblin")


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
    def set_name_options(names):
        Human.name_options = names

    @staticmethod
    def set_adjective_options(adjectives):
        Human.adjective_options = adjectives

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
