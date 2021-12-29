from __future__ import annotations
from typing import Optional

from creature_groups import CreatureGroup
from human import Human


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
