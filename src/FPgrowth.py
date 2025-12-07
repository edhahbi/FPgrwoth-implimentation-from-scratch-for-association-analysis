"""FP-Growth algorithm utilities.

Provides simple preprocessing and mining helpers used by the
accompanying example. The refactor below focuses on clarity and
comments while keeping the original behaviour.
"""

from FPTree import FPTree
from DynamicArray import DynamicArray
from HashMap import HashMap
from FrozenArray import FrozenArray


def preprocess_transactions(transactions, min_sup=2):
    """Filter and group transactions by support.

    Returns a `HashMap` mapping `FrozenArray(transaction)` -> count,
    where transactions only contain items meeting `min_sup` and are
    ordered by descending frequency.
    """
    freq = HashMap()
    for transaction in transactions:
        for item in transaction:
            freq[item] = freq.get(item, 0) + 1

    # keep only frequent items
    frequent = HashMap()
    for pair in freq.get_items():
        if pair.second >= min_sup:
            frequent[pair.first] = pair.second

    grouped = HashMap()
    for transaction in transactions:
        filtered = [item for item in transaction if frequent.get(item, 0) >= min_sup]
        # order by global frequency (descending) for FP-growth
        filtered = sorted(filtered, key=lambda x: frequent[x], reverse=True)

        if filtered:
            key = FrozenArray(filtered)
            grouped[key] = grouped.get(key, 0) + 1

    return grouped


def prefix_paths(base_item, header_table):
    """Return grouped prefix paths for `base_item` as a HashMap.

    The result maps `FrozenArray(path)` -> count where `path` is the
    sequence of items (nearest ancestor first) leading to an instance
    of `base_item` in the FP-tree.
    """
    paths = HashMap()

    for node in header_table[base_item]:
        count = node.count
        path = DynamicArray()
        current = node.parent

        while current and current.item is not None:
            path.append(current.item)
            current = current.parent

        if len(path) > 0:
            path.reverse()
            frozen_path = FrozenArray(path)
            paths[frozen_path] = paths.get(frozen_path, 0) + count

    return paths


def mine_tree(tree: FPTree, suffix, patterns):
    """Recursively mine frequent patterns from an FP-tree.

    `suffix` is a DynamicArray representing the current suffix, and
    `patterns` is a HashMap where mined patterns are accumulated.
    """
    items = DynamicArray()
    for item in tree._frequency_list.get_keys():
        items.append(item)

    # visit items in increasing frequency order (per typical fp-growth)
    items.sort(key=lambda x: tree._frequency_list[x])

    for item in items:
        # build new suffix (copy previous suffix + current item)
        new_suffix = DynamicArray()
        for s in suffix:
            new_suffix.append(s)
        new_suffix.append(item)

        patterns[FrozenArray(new_suffix)] = tree._frequency_list[item]

        cond_paths = prefix_paths(item, tree._header_table)
        if len(cond_paths) == 0:
            continue

        cond_tree = FPTree(cond_paths, tree._min_sup)

        if len(cond_tree._frequency_list.get_keys()) > 0:
            mine_tree(cond_tree, new_suffix, patterns)

    return patterns


def fpgrowth(transactions, min_sup=2):
    """Run FP-growth on grouped transactions and print patterns.

    The function expects `transactions` to be the grouped form returned
    by `preprocess_transactions` (a `HashMap`). It prints discovered
    frequent patterns and their supports.
    """
    tree = FPTree(transactions, min_sup)
    suffix = DynamicArray()
    patterns = HashMap()

    result = mine_tree(tree, suffix, patterns)

    for frequent_list in result.get_items():
        print(frequent_list.first, "->", frequent_list.second)


