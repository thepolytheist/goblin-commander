import goblincommander.creatures
from fixed_random import fixed_random
from goblincommander.creatures import get_stat_rating, get_adjective
from goblincommander.stats import StatKey, BeefStat, CunningStat, QuicknessStat, ReputationStat

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
    stats = {
        StatKey.BEEF: BeefStat(10),
        StatKey.CUNNING: CunningStat(10),
        StatKey.QUICKNESS: QuicknessStat(10),
        StatKey.REPUTATION: ReputationStat(5.0)
    }
    assert get_adjective(stats, 4, 6, 4, 6, 4, 6) == "generic"
