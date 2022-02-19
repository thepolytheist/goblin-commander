import json
from importlib.resources import files
from random import choice, randint

from termcolor import colored

import goblincommander.resources
from goblincommander.creature_groups import Militia
from goblincommander.creatures import Human
from goblincommander.stash import Stash


class Settlement:
    """Model representing a human settlement"""

    settlement_config: dict[str, dict] = json.loads(
        files(goblincommander.resources).joinpath('settlement_data.json').read_text())

    def __init__(self, settlement_type: str,
                 minimum_militia_size: int,
                 maximum_militia_size: int,
                 minimum_food_reward_multiplier: int,
                 maximum_food_reward_multiplier: int,
                 minimum_gold_reward_multiplier: int,
                 maximum_gold_reward_multiplier: int):
        self.name = choice(Settlement.settlement_config[settlement_type]["name_options"])
        self.description = choice(Settlement.settlement_config[settlement_type]["description_options"])
        self.settlement_type = settlement_type
        self.defeated = False
        self.scouted = False

        self.minimum_militia_size = minimum_militia_size
        self.maximum_militia_size = maximum_militia_size

        self.minimum_food_reward_multiplier = minimum_food_reward_multiplier
        self.maximum_food_reward_multiplier = maximum_food_reward_multiplier
        self.minimum_gold_reward_multiplier = minimum_gold_reward_multiplier
        self.maximum_gold_reward_multiplier = maximum_gold_reward_multiplier

        self.militia = Militia.generate_militia(minimum_size=minimum_militia_size,
                                                maximum_size=maximum_militia_size)
        self.reward = Stash(food=randint(minimum_food_reward_multiplier,
                                         maximum_food_reward_multiplier) * len(self.militia.members),
                            gold=randint(minimum_gold_reward_multiplier,
                                         maximum_gold_reward_multiplier) * len(self.militia.members))

    def __str__(self):
        return f"{self.name}, a {self.settlement_type}."

    def get_raid_menu_description(self):
        description = f"{self.name}, a {self.settlement_type} guarded by {len(self.militia.members)} men."

        if self.scouted:
            report = f"(Beef: {self.militia.get_total_beef()}," \
                     f" reward: {self.reward.food} food, {self.reward.gold} gold)"
        else:
            expected_beef = sum([Human.MINIMUM_BEEF, Human.MAXIMUM_BEEF]) / 2 * len(self.militia.members)
            expected_food = sum([self.minimum_food_reward_multiplier,
                                 self.maximum_food_reward_multiplier]) / 2 * len(self.militia.members)
            expected_gold = sum([self.minimum_gold_reward_multiplier,
                                 self.maximum_gold_reward_multiplier]) / 2 * len(self.militia.members)
            report = f"(expected Beef: {expected_beef}, expected reward: {expected_food} food, {expected_gold} gold)"

        return f"{description} {colored(report, attrs=['dark'])}"


class NomadEncampment(Settlement):
    """A small camp of roaming humans."""

    def __init__(self):
        super().__init__(settlement_type="nomad encampment",
                         minimum_militia_size=2,
                         maximum_militia_size=4,
                         minimum_food_reward_multiplier=5,
                         maximum_food_reward_multiplier=15,
                         minimum_gold_reward_multiplier=1,
                         maximum_gold_reward_multiplier=5)


class QuietVillage(Settlement):
    """A quiet, picturesque human village."""

    def __init__(self):
        super().__init__(settlement_type="quiet village",
                         minimum_militia_size=3,
                         maximum_militia_size=8,
                         minimum_food_reward_multiplier=10,
                         maximum_food_reward_multiplier=20,
                         minimum_gold_reward_multiplier=2,
                         maximum_gold_reward_multiplier=6)


class BusyTown(Settlement):
    """A busy merchant town just waiting to be raided."""

    def __init__(self):
        super().__init__(settlement_type="busy town",
                         minimum_militia_size=4,
                         maximum_militia_size=10,
                         minimum_food_reward_multiplier=12,
                         maximum_food_reward_multiplier=24,
                         minimum_gold_reward_multiplier=3,
                         maximum_gold_reward_multiplier=7)


class BustlingCity(Settlement):
    """A bustling city in the shadow of the capital."""

    def __init__(self):
        super().__init__(settlement_type="bustling city",
                         minimum_militia_size=6,
                         maximum_militia_size=15,
                         minimum_food_reward_multiplier=15,
                         maximum_food_reward_multiplier=35,
                         minimum_gold_reward_multiplier=4,
                         maximum_gold_reward_multiplier=9)


class GleamingCastle(Settlement):
    """A bright castle bristling with defenses."""

    def __init__(self):
        super().__init__(settlement_type="gleaming castle",
                         minimum_militia_size=10,
                         maximum_militia_size=30,
                         minimum_food_reward_multiplier=20,
                         maximum_food_reward_multiplier=40,
                         minimum_gold_reward_multiplier=6,
                         maximum_gold_reward_multiplier=10)
