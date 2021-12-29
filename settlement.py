from random import choice

from militia import Militia


class Settlement:
    """Model representing a human settlement"""

    name_options = ["Settleburg", "Settletopia", "Metropolisettle", "Camesettle"]

    def __init__(self):
        self.name = choice(Settlement.name_options)
        self.militia = Militia.generate_militia()

    def __str__(self):
        return f"The settlement of {self.name}, guarded by {len(self.militia.members)} men."
