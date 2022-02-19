from __future__ import annotations


class Stash:
    """Represents a collection of resources."""

    def __init__(self, food: int, gold: int):
        self.food = food
        self.gold = gold

    def add(self, other: Stash):
        self.food += other.food
        self.gold += other.gold

    def __add__(self, other: Stash) -> Stash:
        self.add(other)
        return self
