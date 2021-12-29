from random import choice, randint

from militia import Militia


class Settlement:
    """Model representing a human settlement"""

    name_options = ["Settleburg", "Settletopia", "Metropolisettle", "Camesettle"]

    def __init__(self):
        self.name = choice(Settlement.name_options)
        self.militia = Militia.generate_militia()
        # TODO: Make this based on settlement type instead of just militia size
        self.defeated = False
        self.reward = {"gold": randint(3, 7) * len(self.militia.members),
                       "food": randint(15, 35) * len(self.militia.members)}

    def __str__(self):
        return f"The settlement of {self.name}, guarded by {len(self.militia.members)} men."
