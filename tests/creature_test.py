import goblincommander.creatures
from fixed_random import fixed_random
from goblincommander.creatures import get_stat_rating, get_adjective
from goblincommander.stats import Stats

ADJECTIVES = {
    "generic": ["generic"],
    "strong": ["strong"],
    "weak": ["weak"],
    "smart": ["smart"],
    "dumb": ["dumb"],
    "fast": ["fast"],
    "slow": ["slow"],
    "popular": ["popular"],
    "unpopular": ["unpopular"],
    "rounded": ["rounded"],
    "useless": ["useless"],
    "himbo": ["himbo"]
}


def test_get_stat_rating():
    assert get_stat_rating(5, 4, 6) == 0.5


@fixed_random(123)
def test_get_adjective():
    goblincommander.creatures.adjectives = ADJECTIVES
    stats = Stats(10, 10, 10, 5.0)
    assert get_adjective(stats, 4, 6, 4, 6, 4, 6) == "generic"
