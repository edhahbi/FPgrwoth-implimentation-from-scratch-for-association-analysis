"""Pair helper.

Provides a small lightweight Pair container used by the project's
`HashMap` implementation. Kept minimal and immutable-like using
``__slots__`` for memory efficiency.
"""

class Pair:
    __slots__ = ("first", "second")

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"Pair({self.first!r}, {self.second!r})"

    def __str__(self):
        return f"{self.first} {self.second}"
