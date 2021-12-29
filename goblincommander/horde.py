from __future__ import annotations

from random import randint
from typing import Optional

from creature_groups import CreatureGroup
from goblin import Goblin
from settlement import Settlement
from stats import StatKey


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

    def raid(self, settlement: Settlement) -> Settlement:
        if settlement.defeated or not settlement.militia:
            raise ValueError("Raid target is not a valid settlement for raiding.")

        # TODO: Move these calculations to CreatureGroup
        horde_beef = sum([m.stats[StatKey.BEEF].value for m in self.members])
        horde_cunning = sum([m.stats[StatKey.CUNNING].value for m in self.members])
        horde_quickness = sum([m.stats[StatKey.QUICKNESS].value for m in self.members])
        horde_reputation = sum([m.stats[StatKey.REPUTATION].value for m in self.members])

        militia_beef = sum([m.stats[StatKey.BEEF].value for m in settlement.militia.members])
        militia_cunning = sum([m.stats[StatKey.CUNNING].value for m in settlement.militia.members])
        militia_quickness = sum([m.stats[StatKey.QUICKNESS].value for m in settlement.militia.members])

        print(f"Base horde strength: {horde_beef}")
        print(f"Base militia strength: {militia_beef}")

        if horde_reputation / len(self.members) > 9:
            print(f"\nThe {settlement.name} defense is losing their wits in the face of your famous might.")
            militia_cunning *= 0.7
            print(f"Adjusted horde strength: {horde_beef:.2f}")
            print(f"Adjusted militia strength: {militia_beef:.2f}")

        if horde_quickness / len(self.members) > militia_quickness / len(settlement.militia.members):
            print(f"\nYour speedy horde got the drop on the {settlement.name} defenses! You've caught them unprepared.")
            militia_beef *= 0.9
        else:
            print(f"\nUh oh. The {settlement.name} defenses rallied their forces in record time."
                  " You've got your work cut out for you.")
            horde_beef *= 0.9

        print(f"Adjusted horde strength: {horde_beef:.2f}")
        print(f"Adjusted militia strength: {militia_beef:.2f}")

        if horde_cunning / len(self.members) > militia_cunning / len(settlement.militia.members):
            print(f"\nThe {settlement.name} defenses don't seem too bright. Let's show them who's boss.")
            horde_beef *= 1.1
        else:
            print(f"\nHmm. These men defending {settlement.name} are smarter than we thought."
                  " Best keep our heads on straight.")
            militia_beef *= 1.1

        print(f"Adjusted horde strength: {horde_beef:.2f}")
        print(f"Adjusted militia strength: {militia_beef:.2f}")
        if horde_beef > militia_beef:
            print(f"\nYour horde defeated the pitiful defenses of {settlement.name}.")
            settlement.defeated = True
            settlement.militia.members = []
            self.bolster()
        else:
            print(f"\nYour pitiful horde was defeated by the defenses of {settlement.name}. "
                  "Half of them didn't make it back.")
            self.members = [m for i, m in enumerate(self.members) if i % 2 == 0]
        return settlement

    def bolster(self):
        num_new_goblins = randint(1, 3)
        print(f"You've attracted {num_new_goblins} new goblins!")
        new_goblins = [Goblin() for _ in range(num_new_goblins)]
        self.members.extend(new_goblins)
        print(f"Your horde now boasts {len(self.members)} in its ranks!")
