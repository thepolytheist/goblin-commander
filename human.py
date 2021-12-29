from random import randint, choice

from creature import Creature
from stats import StatKey, BeefStat, CunningStat, QuicknessStat, ReputationStat
from upkeep import Upkeep


class Human(Creature):
    """Model representing an individual Human protecting a settlement.py."""
    
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
