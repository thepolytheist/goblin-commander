from random import choice, randint

from creature import Creature
from stats import BeefStat, CunningStat, QuicknessStat, ReputationStat, StatKey
from upkeep import Upkeep


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
