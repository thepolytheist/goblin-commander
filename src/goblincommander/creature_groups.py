from __future__ import annotations

from random import choices, randint
from typing import Type, TypeVar, Optional

from goblincommander.creatures import Creature, Goblin, Human
from goblincommander.upkeep import Upkeep

G = TypeVar('G')


def generate(creature_group_cls: Type[G],
             creature_types,
             minimum_size: int,
             maximum_size: int,
             type_weights=None,
             commander=None) -> G:
    # Validate range specification, coercing if necessary
    if minimum_size > maximum_size:
        minimum_size, maximum_size = maximum_size, minimum_size
    minimum_size = max(minimum_size, 1)
    maximum_size = max(maximum_size, minimum_size)

    group = creature_group_cls()
    generated_creature_types = choices(creature_types, type_weights, k=randint(minimum_size, maximum_size))
    group.members = [creature_type() for creature_type in generated_creature_types]
    if commander:
        group.members.append(commander)
    return group


class CreatureGroup:
    """Base class for various groups of creatures."""

    def __init__(self, creature_type: Type[Creature], commander: Optional[Creature] = None):
        self.members: list[creature_type] = []
        self.commander = commander

    def get_upkeep(self) -> Upkeep:
        return Upkeep(food=sum([g.upkeep.food for g in self.members]),
                      gold=sum([g.upkeep.gold for g in self.members]))

    def get_total_beef(self) -> int:
        return sum([m.stats.beef.value for m in self.members])

    def get_avg_beef(self) -> float:
        return self.get_total_beef() / len(self.members)

    def get_total_cunning(self) -> int:
        return sum([m.stats.cunning.value for m in self.members])

    def get_avg_cunning(self) -> float:
        return self.get_total_cunning() / len(self.members)

    def get_total_quickness(self) -> int:
        return sum([m.stats.quickness.value for m in self.members])

    def get_avg_quickness(self) -> float:
        return self.get_total_quickness() / len(self.members)

    def get_total_reputation(self) -> float:
        return sum([m.stats.reputation.value for m in self.members])

    def get_avg_reputation(self) -> float:
        return self.get_total_reputation() / len(self.members)


class Horde(CreatureGroup):
    """Model representing a collection of Goblins"""

    def __init__(self):
        super().__init__(Goblin)

    def bolster(self, new_creatures: list[Creature]):
        """
        Adds the specified creatures to the horde's members.
        """
        self.members.extend(new_creatures)

    def cull(self, creatures_to_remove: list[Creature]):
        """
        Removes the specified creatures from the horde.
        """
        for c in creatures_to_remove:
            self.members.remove(c)


def generate_horde(minimum_size: Optional[int] = None,
                   maximum_size: Optional[int] = None,
                   commander: Optional[Creature] = None) -> Horde:
    """Returns a new Horde with a number of Goblins between minimum_size and maximum_size."""
    if minimum_size is None:
        minimum_size = 1
    if maximum_size is None:
        maximum_size = 10

    return generate(Horde, [Goblin], minimum_size, maximum_size, commander=commander)


class Militia(CreatureGroup):
    """Model representing a Settlement's defense force"""

    def __init__(self):
        super().__init__(Human)


def generate_militia(minimum_size: Optional[int] = None, maximum_size: Optional[int] = None) -> Militia:
    """Returns a new Militia with a number of Humans between minimum_size and maximum_size."""
    if minimum_size is None:
        minimum_size = 4
    if maximum_size is None:
        maximum_size = 15

    return generate(Militia, [Human], minimum_size, maximum_size)
