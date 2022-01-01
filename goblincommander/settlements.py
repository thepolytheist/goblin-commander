from random import choice, randint

from creature_groups import Militia


class Settlement:
    """Model representing a human settlement"""

    name_options = ["Settleburg", "Settletopia", "Metropolisettle", "Camesettle"]

    def __init__(self):
        self.name = choice(Settlement.name_options)
        self.defeated = False
        self.militia: Militia = Militia()
        self.reward: dict[str, int] = {}

    def __str__(self):
        return f"The settlement of {self.name}, guarded by {len(self.militia.members)} men."


class NomadEncampment(Settlement):
    """A small camp of roaming humans."""

    def __init__(self):
        super().__init__()
        self.militia = Militia.generate_militia(minimum_size=2, maximum_size=4)
        self.reward = {"gold": randint(1, 5) * len(self.militia.members),
                       "food": randint(5, 15) * len(self.militia.members)}

    def __str__(self):
        return f"{self.name}, a small camp away from civilization. (Militia: {len(self.militia.members)} men)"


class QuietVillage(Settlement):
    """A quiet, picturesque human village."""

    def __init__(self):
        super().__init__()
        self.militia = Militia.generate_militia(minimum_size=3, maximum_size=8)
        self.reward = {"gold": randint(2, 6) * len(self.militia.members),
                       "food": randint(10, 20) * len(self.militia.members)}

    def __str__(self):
        return f"{self.name}, a quiet village. (Militia: {len(self.militia.members)} men)"


class BusyTown(Settlement):
    """A busy merchant town just waiting to be raided."""

    def __init__(self):
        super().__init__()
        self.militia = Militia.generate_militia(minimum_size=4, maximum_size=10)
        self.reward = {"gold": randint(3, 7) * len(self.militia.members),
                       "food": randint(12, 24) * len(self.militia.members)}

    def __str__(self):
        return f"{self.name}, a busy merchant town. (Militia: {len(self.militia.members)} men)"


class BustlingCity(Settlement):
    """A bustling city in the shadow of the capital."""

    def __init__(self):
        super().__init__()
        self.militia = Militia.generate_militia(minimum_size=6, maximum_size=15)
        self.reward = {"gold": randint(4, 9) * len(self.militia.members),
                       "food": randint(15, 35) * len(self.militia.members)}

    def __str__(self):
        return f"{self.name}, a city second only to the capital. (Militia: {len(self.militia.members)} men)"


class GleamingCastle(Settlement):
    """A bright castle bristling with defenses."""

    def __init__(self):
        super().__init__()
        self.militia = Militia.generate_militia(minimum_size=10, maximum_size=30)
        self.reward = {"gold": randint(6, 10) * len(self.militia.members),
                       "food": randint(20, 40) * len(self.militia.members)}

    def __str__(self):
        return f"{self.name}, a bright castle standing tall. (Militia: {len(self.militia.members)} men)"
