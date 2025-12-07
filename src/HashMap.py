"""A compact open-addressing HashMap used by the FP-Growth demo.

This is a small, custom hashmap tuned for the project. The goal of
this refactor is readability; behaviour and public API remain the
same.
"""

from Pair import Pair
from DynamicArray import DynamicArray


class HashMap:
    TOMBSTONE = object()
    __slots__ = ("_container", "_capacity", "_size", "_load_factor")

    def __init__(self, init_cap=8, load_factor=0.66):
        self._capacity = init_cap
        self._size = 0
        self._container = [None] * init_cap
        self._load_factor = load_factor

    def _hash(self, key):
        return hash(key) & 0x7FFFFFFF

    def _find_slot(self, key):
        mask = self._capacity - 1
        perturb = self._hash(key)
        index = perturb & mask
        first_tomb = None

        while True:
            entry = self._container[index]
            if entry is None:
                return first_tomb if first_tomb is not None else index
            if entry is self.TOMBSTONE:
                if first_tomb is None:
                    first_tomb = index
            elif entry.first == key:
                return index

            index = (index * 5 + 1 + perturb) & mask
            perturb >>= 5

    def _rehash(self):
        old_slots = self._container
        self._capacity *= 2
        self._container = [None] * self._capacity
        self._size = 0

        for pair in old_slots:
            if pair is not None and pair is not self.TOMBSTONE:
                self._insert(pair)

    def _insert(self, pair):
        # ensure there's room for one more element before inserting
        if self._size + 1 > self._capacity * self._load_factor:
            self._rehash()

        index = self._find_slot(pair.first)
        current = self._container[index]

        if current is None or current is self.TOMBSTONE:
            self._container[index] = pair
            self._size += 1
        else:
            # replace existing
            self._container[index] = pair

    def __setitem__(self, key, value):
        self._insert(Pair(key, value))

    def __getitem__(self, key):
        index = self._find_slot(key)
        pair = self._container[index]
        if pair is None or pair is self.TOMBSTONE:
            raise KeyError(key)
        return pair.second

    def __len__(self):
        return self._size

    def get(self, key, default=None):
        index = self._find_slot(key)
        pair = self._container[index]
        if pair is None or pair is self.TOMBSTONE:
            return default
        return pair.second

    def __iter__(self):
        for pair in self._container:
            if pair is not None and pair is not self.TOMBSTONE:
                yield pair

    def get_values(self):
        values = DynamicArray()
        for pair in self:
            values.append(pair.second)
        return values

    def get_keys(self):
        keys = DynamicArray()
        for pair in self:
            keys.append(pair.first)
        return keys

    def get_items(self):
        pairs = DynamicArray()
        for pair in self:
            pairs.append(pair)
        return pairs

    def __repr__(self):
        items = ", ".join(f"{p.first}: {p.second}" for p in self)
        return "{" + items + "}"


if __name__ == '__main__':
    h = HashMap()
    h[1] = 2
    h[3] = 4
    h[2] = 5

    print("h[1] =", h[1])
    print("All keys:", list(h.get_keys()))
    print("All values:", list(h.get_values()))
    print("All pairs:", [(p.first, p.second) for p in h.get_items()])
    print("HashMap:", h)
