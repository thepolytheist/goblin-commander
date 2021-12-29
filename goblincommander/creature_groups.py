from __future__ import annotations
from random import choices, randint
from tabulate import tabulate
from typing import Type, TypeVar

from creature import Creature
from stats import StatKey
from upkeep import Upkeep

G = TypeVar('G')


class CreatureGroup:
    """Base class for various groups of creatures."""

    @staticmethod
    def generate(creature_group_cls: Type[G],
                 creature_types,
                 minimum_size: int,
                 maximum_size: int,
                 type_weights=None) -> G:
        # Validate range specification, coercing if necessary
        if minimum_size > maximum_size:
            minimum_size, maximum_size = maximum_size, minimum_size
        minimum_size = max(minimum_size, 1)
        maximum_size = max(maximum_size, minimum_size)

        group = creature_group_cls()
        generated_creature_types = choices(creature_types, type_weights, k=randint(minimum_size, maximum_size))
        group.members = [creature_type() for creature_type in generated_creature_types]
        return group

    def __init__(self, creature_type: Type[Creature]):
        self.members: list[creature_type] = []

    def get_upkeep(self) -> Upkeep:
        return Upkeep(food=sum([g.upkeep.food for g in self.members]),
                      gold=sum([g.upkeep.gold for g in self.members]))

    def print_members(self):
        print(tabulate([[creature.name, type(creature).__name__, creature.adjective,
                         str(creature.stats[StatKey.BEEF].value),
                         str(creature.stats[StatKey.CUNNING].value),
                         str(creature.stats[StatKey.QUICKNESS].value),
                         f"{creature.stats[StatKey.REPUTATION].value:.2f}"] for creature in self.members],
                       headers=["Name", "Type", "Adjective", "Beef", "Cunning", "Quickness", "Reputation"]))
