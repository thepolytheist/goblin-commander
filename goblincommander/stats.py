from enum import Enum, auto


class StatKey(str, Enum):
    BEEF = "beef"
    CUNNING = "cunning"
    QUICKNESS = "quickness"
    REPUTATION = "reputation"


class Stat:
    """Base creature stat class"""

    def __init__(self, name: str, short_name: str, description: str, key: StatKey, value: int | float):
        self.name = name
        self.short_name = short_name
        self.description = description
        self.key = key
        self.value = value


class BeefStat(Stat):
    """Beef creature stat"""

    def __init__(self, value: int):
        super().__init__("Beef", "BF", "A creature's strength and hardiness.",
                         StatKey.BEEF, value)


class CunningStat(Stat):
    """Cunning creature stat"""

    def __init__(self, value: int):
        super().__init__("Cunning", "CUN", "A creature's mental sharpness and aptitude for conniving.",
                         StatKey.CUNNING, value)


class QuicknessStat(Stat):
    """Quickness creature stat"""

    def __init__(self, value: int):
        super().__init__("Quickness", "QCK", "A creature's physical speed and circus capabilities.",
                         StatKey.QUICKNESS, value)


class ReputationStat(Stat):
    """Reputation creature stat"""

    def __init__(self, value: float):
        super().__init__("Reputation", "REP", "A creature's status among goblins and other creatures.",
                         StatKey.REPUTATION, value)
