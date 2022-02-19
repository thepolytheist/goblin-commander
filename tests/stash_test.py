from goblincommander.stash import Stash


def test_stash_add():
    stash1 = Stash(5, 5)
    stash2 = Stash(1, 2)
    stash1.add(stash2)
    assert stash1.food == 6
    assert stash1.gold == 7

    stash1 += stash2

    assert stash1.food == 7
    assert stash1.gold == 9
