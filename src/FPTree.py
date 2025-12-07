"""FP-tree implementation used by the FP-Growth algorithm.

This module provides a minimal FPTree class and its internal node
structure. The implementation is intentionally small and tuned for
readability rather than feature completeness.
"""

from HashMap import HashMap
from DynamicArray import DynamicArray
from FrozenArray import FrozenArray
from LinkedList import LinkedList


class FPTree:
    class FPNode:
        __slots__ = ("item", "count", "parent", "children")

        def __init__(self, item, count, parent):
            self.item = item
            self.count = count
            self.parent = parent
            self.children = HashMap()

        def increment(self, count=1):
            self.count += count

        def __repr__(self):
            return f"FPNode({self.item!r}, count={self.count})"

    def __init__(self, grouped_transactions: HashMap, min_sup=2):
        self._root = self.FPNode(None, 0, None)
        self._header_table = HashMap()
        self._frequency_list = HashMap()
        self._min_sup = min_sup

        # Build internal tables and tree from grouped transactions
        item_counts = self._count_items_frequency(grouped_transactions)
        self._filter_by_support(item_counts)
        self._build_header_table()
        self._build_tree(grouped_transactions)

    def _count_items_frequency(self, grouped_transactions):
        freq = HashMap()
        for pair in grouped_transactions.get_items():
            transaction, count = pair.first, pair.second
            for item in transaction:
                freq[item] = freq.get(item, 0) + count
        return freq

    def _filter_by_support(self, item_counts):
        for pair in item_counts.get_items():
            if pair.second >= self._min_sup:
                self._frequency_list[pair.first] = pair.second

    def _build_header_table(self):
        for pair in self._frequency_list.get_items():
            self._header_table[pair.first] = LinkedList()

    def _insert_transaction(self, transaction, count):
        parent = self._root
        for item in transaction:
            if self._frequency_list.get(item, 0) < self._min_sup:
                continue  # skip infrequent items

            child = parent.children.get(item, None)
            if child is None:
                child = self.FPNode(item, count, parent)
                parent.children[item] = child
                self._header_table[item].append(child)
            else:
                child.increment(count)

            parent = child

    def _build_tree(self, grouped_transactions):
        for pair in grouped_transactions.get_items():
            transaction, count = pair.first, pair.second
            self._insert_transaction(transaction, count)

    def print_tree(self, node=None, indent=0):
        if node is None:
            node = self._root
        for child_pair in node.children.get_items():
            child = child_pair.second
            print("  " * indent + f"{child.item} ({child.count})")
            self.print_tree(child, indent + 1)
