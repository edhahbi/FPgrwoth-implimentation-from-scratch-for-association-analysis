class DynamicArray:
    """A lightweight dynamic array.

    This mimics the subset of Python's list API needed by the project
    (append, indexing, iteration, sort, reverse) while keeping the
    underlying implementation explicit for educational purposes.
    """

    __slots__ = ("_size", "_capacity", "_container", "_load_factor")

    def __init__(self, init_capacity=8, load_factor=0.66):
        self._size = 0
        self._capacity = init_capacity
        self._container = [None] * init_capacity
        self._load_factor = load_factor

    def _insert(self, value, index):
        if self._size / self._capacity > self._load_factor:
            self._resize()
        if 0 <= index < self._capacity:
            if self._container[index] is None:
                self._size += 1
            self._container[index] = value
            return
        raise IndexError(f"index {index} out of range")

    def append(self, value):
        self._insert(value, self._size)

    def _resize(self):
        old_container = self._container
        self._capacity *= 2
        self._container = [None] * self._capacity
        old_size = self._size
        self._size = 0
        for value in old_container:
            if value is not None:
                self.append(value)
        self._size = old_size

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        if 0 <= index < self._size:
            return self._container[index]
        raise IndexError(f"index {index} out of range")

    def __setitem__(self, index, value):
        self._insert(value, index)

    def __iter__(self):
        for index in range(self._size):
            yield self._container[index]

    def reverse(self):
        self._container[: self._size] = self._container[: self._size][::-1]

    def sort(self, key=None, reverse=False):
        self._container[: self._size] = sorted(
            self._container[: self._size], key=key, reverse=reverse
        )

    def clear(self):
        self._container = [None] * self._capacity
        self._size = 0

    def __repr__(self):
        return f"DynamicArray({[self._container[i] for i in range(self._size)]})"
