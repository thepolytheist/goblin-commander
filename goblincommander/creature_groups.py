from __future__ import annotations

from random import choices, randint
from typing import Type, TypeVar, Optional

from tabulate import tabulate

from creatures import Creature, Goblin, Human
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


class Horde(CreatureGroup):
    """Model representing a collection of Goblins"""

    @staticmethod
    def generate_horde(minimum_size: Optional[int] = None, maximum_size: Optional[int] = None) -> Horde:
        """Returns a new Horde with a number of Goblins between minimum_size and maximum_size."""
        if minimum_size is None:
            minimum_size = 1
        if maximum_size is None:
            maximum_size = 10

        return CreatureGroup.generate(Horde, [Goblin], minimum_size, maximum_size)

    def __init__(self):
        super().__init__(Goblin)

    def bolster(self):
        num_new_goblins = randint(1, 3)
        print(f"You've attracted {num_new_goblins} new goblins!")
        new_goblins = [Goblin() for _ in range(num_new_goblins)]
        self.members.extend(new_goblins)
        print(f"Your horde now boasts {len(self.members)} in its ranks!")


class Militia(CreatureGroup):
    """Model representing a Settlement's defense force"""

    @staticmethod
    def generate_militia(minimum_size: Optional[int] = None, maximum_size: Optional[int] = None) -> Militia:
        """Returns a new Militia with a number of Humans between minimum_size and maximum_size."""
        if minimum_size is None:
            minimum_size = 4
        if maximum_size is None:
            maximum_size = 15

        return CreatureGroup.generate(Militia, [Human], minimum_size, maximum_size)

    def __init__(self):
        super().__init__(Human)
