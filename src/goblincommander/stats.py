class Stat:
    """Base creature stat class"""

    def __init__(self, name: str, short_name: str, description: str, value: int | float):
        self.name = name
        self.short_name = short_name
        self.description = description
        self.value = value


class BeefStat(Stat):
    """Beef creature stat"""

    def __init__(self, value: int):
        super().__init__("Beef", "BF", "A creature's strength and hardiness.", value)


class CunningStat(Stat):
    """Cunning creature stat"""

    def __init__(self, value: int):
        super().__init__("Cunning", "CUN", "A creature's mental sharpness and aptitude for conniving.", value)


class QuicknessStat(Stat):
    """Quickness creature stat"""

    def __init__(self, value: int):
        super().__init__("Quickness", "QCK", "A creature's physical speed and circus capabilities.", value)


class ReputationStat(Stat):
    """Reputation creature stat"""

    def __init__(self, value: float):
        super().__init__("Reputation", "REP", "A creature's status among goblins and other creatures.", value)


class Stats:
    def __init__(self, beef: int, cunning: int, quickness: int, reputation: float):
        self.beef = BeefStat(beef)
        self.cunning = CunningStat(cunning)
        self.quickness = QuicknessStat(quickness)
        self.reputation = ReputationStat(reputation)
