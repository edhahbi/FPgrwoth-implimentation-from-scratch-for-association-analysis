from DynamicArray import DynamicArray


class FrozenArray:
    """Hashable, sequence-like wrapper around `DynamicArray`.

    This small helper provides an immutable-seeming container that can
    be used as a hashmap key. Internally it stores items in the
    project's `DynamicArray` but exposes a simple sequence API.
    """

    def __init__(self, arr):
        self.data = DynamicArray()
        for i in arr:
            self.data.append(i)

    def __hash__(self):
        h = 0
        for i in self.data:
            h = (h * 31 + hash(i)) & 0x7FFFFFFF
        return h

    def __eq__(self, other):
        if not isinstance(other, FrozenArray):
            return False
        if len(self.data) != len(other.data):
            return False
        for i in range(len(self.data)):
            if self.data[i] != other.data[i]:
                return False
        return True

    def __iter__(self):
        for i in self.data:
            yield i

    def __repr__(self):
        return "[" + ", ".join(repr(x) for x in self.data) + "]"