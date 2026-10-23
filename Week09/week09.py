# COMP 271 -- Week 09 assignment: linked lists.
#
# Problem 1: A singly linked list that checks itself (_check_invariants, remove_at).
# Problem 2: Two riders (has_loop).
# Problem 3: Clearing the Loop (eliminate_every).
# Problem 4: A doubly linked list (reverse, remove_last).
#
# Everything below is complete except the six methods whose body is a
# single `raise NotImplementedError(...)` line. Replace each of those lines
# with your implementation: the raise is a placeholder, and any method still
# holding one counts as unanswered.
#
# Do not modify any other code, and do not rename anything.
# Run this file (uv run week09.py) to check your work against the expected
# output written beside each print below. Never run it with python -O:
# that flag deletes every assert statement, including the ones you write.


class Node:
    """One station, linked to the station after it."""

    def __init__(self, data: str) -> None:
        # The station name this node carries
        self._data: str = data
        # The following station; None until it is linked
        self._next: Node | None = None

    @property
    def data(self) -> str:
        """Return the station name."""
        return self._data

    @property
    def next(self) -> "Node | None":
        """Return the following station."""
        return self._next

    @next.setter
    def next(self, node: "Node | None") -> None:
        """Link this station to node."""
        self._next = node


# ----- Problems 1 and 2: a singly linked list with a size counter -----


class LinkedList:
    """A train line: Nodes chained from the head, plus a running count."""

    def __init__(self) -> None:
        # The first station; None means an empty line
        self._head: Node | None = None
        # How many stations are on the line, kept up to date by every change
        self._size: int = 0

    def is_empty(self) -> bool:
        """Return True when the line has no stations."""
        return self._head is None

    def size(self) -> int:
        """Return the number of stations, with no ride."""
        return self._size

    def __str__(self) -> str:
        """Return the stations in order, arrow-joined."""
        names: list[str] = []
        current = self._head
        # Ride until we fall off the end of the line
        while current is not None:
            names.append(current.data)
            current = current.next
        return " -> ".join(names)

    def add_first(self, data: str) -> None:
        """Insert data as the new first station."""
        new_node = Node(data)
        # New station points at the old first station, then becomes the head
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def add_last(self, data: str) -> None:
        """Append data as the new last station."""
        new_node = Node(data)
        if self._head is None:
            # Empty line: the new station is the whole line
            self._head = new_node
        else:
            # Ride to the last station, then hook the new one on after it
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def get(self, index: int) -> str:
        """Return the name of the station at index.

        Precondition: 0 <= index < self.size(), or IndexError is raised.
        """
        # The caller's mistake: raise, so it is reported in every run
        if index < 0 or index >= self._size:
            raise IndexError(f"no station at index {index}")
        current = self._head
        # Ride exactly index stops from the head
        for _ in range(index):
            # Our own promise: _size says this station exists
            assert current is not None, "ran off the end of the line"
            current = current.next
        assert current is not None, "ran off the end of the line"
        return current.data

    # ----- Problem 1 -----

    def _check_invariants(self) -> None:
        """Assert that _size matches the number of nodes on the line.

        Ride the whole line, count the nodes, and assert that the count
        equals self._size. Return nothing when the line is healthy; raise
        AssertionError, with a message, when it is not.
        """
        raise NotImplementedError("replace this line with your implementation")

    def remove_at(self, index: int) -> str:
        """Remove the station at index and return its name.

        Precondition: 0 <= index < self.size(); any other index (including
        every index on an empty line) raises IndexError and leaves the line
        unchanged.
        Postconditions: the returned name was the one at index, and the size
        went down by 1.
        """
        raise NotImplementedError("replace this line with your implementation")

    # ----- Problem 2 -----

    def has_loop(self) -> bool:
        """Return True if following next from the head ever revisits a node,
        False if the ride reaches None.

        Use two riders: one moves one stop per turn, the other two. Do not
        read _size or call size() or len(), and do not change any link.
        """
        raise NotImplementedError("replace this line with your implementation")


# ----- Problem 3: a circular list -----


class CircularLinkedList:
    """A loop of stations: the last station links back to the first.

    The list keeps _tail, not _head; the first station is _tail.next.
    """

    def __init__(self) -> None:
        # The last station; None means an empty loop
        self._tail: Node | None = None
        # How many stations are on the loop
        self._size: int = 0

    def is_empty(self) -> bool:
        """Return True when the loop has no stations."""
        return self._tail is None

    def size(self) -> int:
        """Return the number of stations, with no ride."""
        return self._size

    def __str__(self) -> str:
        """Return the stations once around, first to last, arrow-joined."""
        names: list[str] = []
        if self._tail is not None:
            current = self._tail.next
            # Ride once around: stop after the tail has been added
            for _ in range(self._size):
                assert current is not None, "a loop never reaches None"
                names.append(current.data)
                current = current.next
        return " -> ".join(names)

    def add_first(self, data: str) -> None:
        """Insert data before the first station, keeping the loop closed."""
        new_node = Node(data)
        if self._tail is None:
            # A loop of one points at itself
            self._tail = new_node
            new_node.next = new_node
        else:
            # The new station points at the old first, the tail points at it
            new_node.next = self._tail.next
            self._tail.next = new_node
        self._size += 1

    def add_last(self, data: str) -> None:
        """Append data after the last station: add_first, then move _tail."""
        self.add_first(data)
        assert self._tail is not None, "add_first left the loop empty"
        self._tail = self._tail.next

    def _check_invariants(self) -> None:
        """Given: assert that riding once around from the first station
        returns to it after exactly _size stops.
        """
        count = 0
        if self._tail is not None:
            # Ride from the first station until we are back at the tail;
            # stop early past _size so a broken loop cannot ride forever
            current = self._tail.next
            count = 1
            while (current is not None and current is not self._tail
                   and count <= self._size):
                current = current.next
                count += 1
            assert current is self._tail, "the ride never returns to the tail"
        assert count == self._size, f"_size is {self._size}, loop has {count}"

    # ----- Problem 3 -----

    def eliminate_every(self, k: int) -> list[str]:
        """Empty the loop round-robin and return the names in the order
        they were removed.

        Start counting at the first station, which counts as 1. Remove the
        k-th station counted, then start counting again at the station
        after it, going round the loop as many times as needed, until no
        station is left. With k == 1 the stations leave in order.

        A k below 1 raises ValueError. An empty loop returns []. Unlink each
        station by rewiring the station before it: do not create nodes, do
        not call other methods that change the loop, and do not work the
        order out on a Python list first.
        Postconditions: the loop is empty, and every station was removed
        exactly once.
        """
        raise NotImplementedError("replace this line with your implementation")


# ----- Problem 4: a doubly linked list -----


class DoubleNode:
    """One station with links both ways."""

    def __init__(self, data: str) -> None:
        # The station name this node carries
        self._data: str = data
        # The station toward the tail; None at the last station
        self._next: DoubleNode | None = None
        # The station toward the head; None at the first station
        self._prev: DoubleNode | None = None

    @property
    def data(self) -> str:
        """Return the station name."""
        return self._data

    @property
    def next(self) -> "DoubleNode | None":
        """Return the station toward the tail."""
        return self._next

    @next.setter
    def next(self, node: "DoubleNode | None") -> None:
        """Link this station to node, toward the tail."""
        self._next = node

    @property
    def prev(self) -> "DoubleNode | None":
        """Return the station toward the head."""
        return self._prev

    @prev.setter
    def prev(self, node: "DoubleNode | None") -> None:
        """Link this station to node, toward the head."""
        self._prev = node


class DoublyLinkedList:
    """A line that remembers both of its ends."""

    def __init__(self) -> None:
        # The first station; None means an empty line
        self._head: DoubleNode | None = None
        # The last station; None means an empty line
        self._tail: DoubleNode | None = None
        # How many stations are on the line
        self._size: int = 0

    def is_empty(self) -> bool:
        """Return True when the line has no stations."""
        return self._head is None

    def size(self) -> int:
        """Return the number of stations, with no ride."""
        return self._size

    def __str__(self) -> str:
        """Return the stations head to tail, arrow-joined."""
        names: list[str] = []
        current = self._head
        # Ride toward the tail until we fall off the end
        while current is not None:
            names.append(current.data)
            current = current.next
        return " -> ".join(names)

    def add_last(self, data: str) -> None:
        """Append a station after the current tail, with no ride."""
        new_node = DoubleNode(data)
        if self._tail is None:
            # Empty line: the new station is both ends
            self._head = new_node
        else:
            # The new station points back first, then the old tail points forward
            new_node.prev = self._tail
            self._tail.next = new_node
        self._tail = new_node
        self._size += 1

    def _check_invariants(self) -> None:
        """Given: assert that the line agrees with itself.

        Ride from _head toward the tail and assert three things: each
        node's prev is the node the ride just left (None for the head);
        the last node the ride visits is _tail (None on an empty line); and
        the number of nodes equals _size.
        """
        previous = None
        current = self._head
        count = 0
        # Ride toward the tail, checking each backward link on the way
        while current is not None:
            assert current.prev is previous, f"bad prev at {current.data!r}"
            previous = current
            current = current.next
            count += 1
        # The ride must end on the tail, after exactly _size stations
        assert previous is self._tail, "_tail is not the last station"
        assert count == self._size, f"_size is {self._size}, line has {count}"

    # ----- Problem 4 -----

    def reverse(self) -> None:
        """Reverse the line in place: the old tail becomes the head.

        Create no nodes and change no node's data: swap each node's next
        and prev links, then swap _head and _tail. An empty line stays
        empty.
        Postcondition: the old first station is now the last one.
        """
        raise NotImplementedError("replace this line with your implementation")

    def remove_last(self) -> str:
        """Remove the last station and return its name.

        Raise IndexError on an empty line (lecture's version returned None;
        this one fails loudly, like list.pop). Removing the only station
        leaves an empty line. No loop: the tail already knows the station
        before it, so the rewiring takes no ride. (The _check_invariants
        call at the end does ride the line; that is the price of checking.)
        Postcondition: the new tail, if any, links to nothing after it.
        """
        raise NotImplementedError("replace this line with your implementation")


if __name__ == "__main__":
    # Each problem's checks run on their own, so you can work in any order:
    # an unfinished or crashing problem prints one line and the rest still run.

    def error_name(action) -> str:
        """Run action() and return the name of the exception it raises."""
        name = "no error"
        try:
            action()
        except Exception as error:  # noqa: BLE001 -- report any exception by name
            name = type(error).__name__
        return name

    def brown_line() -> LinkedList:
        """Build a four-station Brown Line, north to south."""
        line = LinkedList()
        for station in ["Kimball", "Kedzie", "Francisco", "Rockwell"]:
            line.add_last(station)
        return line

    def problem_1() -> None:
        # ----- Problem 1 -----
        line = brown_line()
        line._check_invariants()                # a healthy line: nothing printed
        print(line.remove_at(2), "|", line)     # expected: Francisco | Kimball -> Kedzie -> Rockwell
        print(line.remove_at(0), line.remove_at(1), "|", line, line.size())
        # expected: Kimball Rockwell | Kedzie 1
        # A bad index is the caller's mistake: IndexError, line unchanged.
        print(error_name(lambda: line.remove_at(1)),
              error_name(lambda: line.remove_at(-1)),
              error_name(lambda: LinkedList().remove_at(0)))
        # expected: IndexError IndexError IndexError
        print(line, line.size())                # expected: Kedzie 1
        # Break the counter on purpose (code outside the class should never
        # touch _size): _check_invariants must catch it.
        line._size = 7
        print(error_name(line._check_invariants))   # expected: AssertionError

    def problem_2() -> None:
        # ----- Problem 2 -----
        line = brown_line()
        print(line.has_loop(), LinkedList().has_loop())     # expected: False False
        # Link the last station back to the second, on purpose, to make a loop.
        # Do not print a line with a loop: __str__ would ride forever.
        # Each assert tells the type checker a node exists, as it does in the class.
        assert line._head is not None, "the line has four stations"
        second = line._head.next
        assert second is not None and second.next is not None, "four stations"
        last = second.next.next
        assert last is not None, "the line has four stations"
        last.next = second
        print(line.has_loop())                  # expected: True

    def problem_3() -> None:
        # ----- Problem 3 -----
        def the_loop() -> CircularLinkedList:
            loop = CircularLinkedList()
            for station in ["Clark/Lake", "State/Lake", "Washington/Wabash",
                            "Adams/Wabash", "Quincy"]:
                loop.add_last(station)
            return loop

        loop = the_loop()
        print(loop)                             # expected: Clark/Lake -> State/Lake -> Washington/Wabash -> Adams/Wabash -> Quincy
        print(loop.eliminate_every(2))
        # expected: ['State/Lake', 'Adams/Wabash', 'Clark/Lake', 'Quincy', 'Washington/Wabash']
        print(loop.is_empty(), loop.size(), repr(str(loop)))     # expected: True 0 ''
        print(the_loop().eliminate_every(1))
        # expected: ['Clark/Lake', 'State/Lake', 'Washington/Wabash', 'Adams/Wabash', 'Quincy']
        print(the_loop().eliminate_every(7))
        # expected: ['State/Lake', 'Quincy', 'Clark/Lake', 'Washington/Wabash', 'Adams/Wabash']
        print(CircularLinkedList().eliminate_every(3),
              error_name(lambda: the_loop().eliminate_every(0)))
        # expected: [] ValueError

    def problem_4() -> None:
        # ----- Problem 4 -----
        orange = DoublyLinkedList()
        for station in ["Midway", "Pulaski", "Kedzie", "Western", "35th/Archer"]:
            orange.add_last(station)
        orange._check_invariants()              # a healthy line: nothing printed
        print(orange.remove_last(), orange)     # expected: 35th/Archer Midway -> Pulaski -> Kedzie -> Western
        orange.reverse()
        print(orange)                           # expected: Western -> Kedzie -> Pulaski -> Midway
        print(orange.remove_last(), orange)     # expected: Midway Western -> Kedzie -> Pulaski
        orange.reverse()
        orange.add_last("Halsted")
        print(orange)                           # expected: Pulaski -> Kedzie -> Western -> Halsted
        for _ in range(4):
            orange.remove_last()
        orange.reverse()
        print(orange.is_empty(), error_name(orange.remove_last))   # expected: True IndexError
        for station in ["Midway", "Pulaski", "Kedzie"]:
            orange.add_last(station)
        # Cut one backward link on purpose: _check_invariants must catch it.
        assert orange._tail is not None, "the line has three stations"
        orange._tail.prev = orange._head
        print(error_name(orange._check_invariants))         # expected: AssertionError

    for check in (problem_1, problem_2, problem_3, problem_4):
        try:
            check()
        except NotImplementedError:
            print(f"{check.__name__}: not finished yet, skipped")
        except Exception as error:  # noqa: BLE001 -- report any crash, keep going
            print(f"{check.__name__}: stopped by {type(error).__name__}: {error}")
