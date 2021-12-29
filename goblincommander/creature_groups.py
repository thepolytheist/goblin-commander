from __future__ import annotations
from random import choices, randint
from typing import Type, TypeVar

from creature import Creature
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
        for creature in self.members:
            print(creature.describe())
