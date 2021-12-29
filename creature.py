from stats import StatKey, Stat
from upkeep import Upkeep


class Creature:
    """Base class representing any creature in a horde"""

    def __init__(self, name: str, adjective: str, stats: dict[StatKey, Stat], upkeep: Upkeep):
        self.name = name
        self.adjective = adjective
        self.stats = stats
        self.upkeep = upkeep

    def describe(self, creature_type: str = "creature") -> str:
        """Gets a basic description string of the creature."""
        return f'A {self.adjective} {creature_type} named {self.name}.'

    def stats_string(self, multiline=True) -> str:
        """Gets a display string of the creature's stats for inline or multiline block printing."""
        stats_list = list(self.stats.values())
        if multiline:
            return '\t'.join([s.short_name for s in stats_list]) + '\n' + \
                   '\t'.join([str(s.value) for s in stats_list])
        return ', '.join([f'{s.short_name}: {s.value}' for s in stats_list])

    def __str__(self):
        return f'{self.describe()}\n{self.stats_string()}'
