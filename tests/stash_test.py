from goblincommander.stash import Stash


def test_stash_add_method():
    stash1 = Stash(5, 5)
    stash2 = Stash(1, 2)
    stash1.add(stash2)
    assert stash1.food == 6
    assert stash1.gold == 7


def test_stash_add_operator():
    stash1 = Stash(5, 5)
    stash2 = Stash(1, 2)
    stash1 = stash1 + stash2

    assert stash1.food == 6
    assert stash1.gold == 7


def test_stash_iadd():
    stash1 = Stash(5, 5)
    stash2 = Stash(1, 2)
    stash1 += stash2

    assert stash1.food == 6
    assert stash1.gold == 7
