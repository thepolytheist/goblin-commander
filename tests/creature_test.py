from goblincommander.creatures import get_stat_rating


def test_get_stat_rating():
    assert get_stat_rating(5, 4, 6) == 0.5
