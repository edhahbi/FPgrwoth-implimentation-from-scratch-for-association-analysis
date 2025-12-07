"""A tiny singly linked list used by the header table.

Only append and iteration are required by the project.
"""


class LinkedList:
    class Node:
        __slots__ = ("data", "next")

        def __init__(self, data):
            self.data = data
            self.next = None

    __slots__ = ("head", "tail")

    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, node):
        """Append a node (commonly an FPNode) in O(1)."""
        new_node = self.Node(node)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
