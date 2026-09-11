# COMP 271 -- Week 03 assignment.
#
# Problem 1: DynamicArray accessors.
# Problem 2: DynamicArray magic methods.
# Problem 3: Cards, properties and decorators.
# Problem 4: Bounded arrays, inheritance and name mangling.
#
# The two classes below, and the decorator that follows them, are complete
# except for the methods and functions whose body is a single
# `raise NotImplementedError(...)` line. Replace each of those lines with
# your implementation -- the raise is a placeholder, and any method still
# holding one counts as unanswered.
#
# Do not modify any other method, and do not rename anything.
# Run this file (uv run week03.py) to check your work against the expected
# output written beside each print below.


class DynamicArray:
    """A fixed-capacity array of non-negative integers that doubles its
    capacity whenever it fills up.
    """

    # Class-level constants: shared by every instance, not stored per object.
    # Naming them documents the policy and keeps the literals out of the code.
    _DEFAULT_CAPACITY: int = 4
    _GROWTH_FACTOR: int = 2
    _EMPTY: int = -1  # sentinel: "this slot holds no value"

    def __init__(self, capacity: int = _DEFAULT_CAPACITY) -> None:
        # A capacity below 1 would leave nowhere to put the first value.
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity: int = capacity
        self._size: int = 0
        # Pre-fill every slot with the sentinel, so the underlying list
        # always holds exactly _capacity entries.
        self._underlying: list[int] = []
        for _ in range(self._capacity):
            self._underlying.append(self._EMPTY)

    def __str__(self) -> str:
        # Show only the filled slots -- sentinel slots are internal detail.
        inside = ""
        for i in range(self._size):
            inside = inside + str(self._underlying[i])
            if i < self._size - 1:
                inside = inside + ", "
        return "[" + inside + "]"

    def resize(self) -> None:
        # Build a bigger array, copy what is real, then swap it in.
        bigger_capacity = self._capacity * self._GROWTH_FACTOR
        temp: list[int] = []
        for _ in range(bigger_capacity):
            temp.append(self._EMPTY)
        # Only the first _size entries hold real values; the rest are
        # already sentinels in temp.
        for i in range(self._size):
            temp[i] = self._underlying[i]
        self._underlying = temp
        self._capacity = bigger_capacity

    def add(self, value: int) -> None:
        # A negative value could not be told apart from the sentinel.
        if value < 0:
            raise ValueError("values must be non-negative")
        # Grow first if the array is full, so index _size is always writable.
        if self._size >= self._capacity:
            self.resize()
        # _size is both the count of values and the index of the next slot.
        self._underlying[self._size] = value
        self._size = self._size + 1

    # ----- Problem 1: accessors -----

    def __len__(self) -> int:
        """Return the number of values stored in this array.

        Makes len(da) work, and with it truthiness checks like `if da:`.
        """
        raise NotImplementedError("replace this line with your implementation")

    def get_size(self) -> int:
        """Return the number of values stored in this array.

        The same number __len__ reports, under a name that does not require
        knowing Python's dunder protocol.
        """
        raise NotImplementedError("replace this line with your implementation")

    def get_capacity(self) -> int:
        """Return the total number of slots in the underlying array,
        including the empty sentinel slots.

        Size is the guest count; capacity is the room count.
        """
        raise NotImplementedError("replace this line with your implementation")

    def get(self, index: int) -> int:
        """Return the value stored at `index`.

        Valid positions are 0 through get_size() - 1. Return _EMPTY for any
        index outside that range, and do not raise.

        Careful: a plain Python list accepts negative indices and counts from
        the end, so get(-1) must be rejected by your own bounds check.
        """
        raise NotImplementedError("replace this line with your implementation")

    def index_of(self, value: int) -> int:
        """Return the position of the first occurrence of `value`, or _EMPTY
        if it is not stored.

        Search the filled slots only. The sentinel slots all hold _EMPTY, so
        searching them would let index_of report a slot that holds nothing.
        """
        raise NotImplementedError("replace this line with your implementation")

    def contains(self, value: int) -> bool:
        """Return True if `value` is stored in this array, False otherwise.

        Write this one in terms of index_of. A second search loop here would
        be the duplicated logic we refactored away in class -- and this
        method is checked for it.
        """
        raise NotImplementedError("replace this line with your implementation")

    def remove(self, value: int) -> bool:
        """Remove the first occurrence of `value`, and report whether
        anything was removed.

        Removing from the middle leaves a hole, so every later value shifts
        one slot to the left. The slot freed at the end must be reset to
        _EMPTY, and the size must shrink by one. Capacity does not change.
        """
        raise NotImplementedError("replace this line with your implementation")

    # ----- Problem 2: magic methods -----

    @classmethod
    def from_values(cls, values: list[int]) -> "DynamicArray":
        """Build and return a new array holding `values`, in order.

        This is an alternative constructor, so it is a @classmethod: it
        receives the class as `cls` rather than an instance as `self`. Build
        the result with cls(), not with DynamicArray() -- called on a
        subclass, cls() produces an instance of that subclass.
        """
        raise NotImplementedError("replace this line with your implementation")

    def __eq__(self, other: object) -> bool:
        """Return True when `other` holds the same values in the same order.

        Capacity is not part of the comparison: two arrays holding the same
        three values are equal even if one has room for four and the other
        for sixty-four.

        Compare type(self) with type(other) rather than using isinstance, so
        that an instance of a subclass is never equal to a plain
        DynamicArray. Comparing against something that is not an array at
        all (a string, None) must return False, not raise.
        """
        raise NotImplementedError("replace this line with your implementation")

    def __repr__(self) -> str:
        """Return a string that could rebuild this object, for example
        `DynamicArray.from_values([10001, 60626])`.

        Where __str__ is for a human reading output, __repr__ is for a
        programmer at the shell, and is what Python shows for an object
        sitting inside a list. Build the name with type(self).__name__
        rather than hardcoding "DynamicArray", so a subclass reports itself.
        """
        raise NotImplementedError("replace this line with your implementation")

    def __add__(self, other: "DynamicArray") -> "DynamicArray":
        """Return a NEW array holding this array's values followed by
        `other`'s. Makes `a + b` work.

        Neither operand may be modified: `a + b` must leave both `a` and `b`
        exactly as they were. Return a plain DynamicArray, since a
        concatenation can be longer than a subclass would allow.
        """
        raise NotImplementedError("replace this line with your implementation")


class Card:
    """One playing card: a rank and a suit that travel together."""

    # The 13 legal ranks, in order. Naming them keeps the check in one place.
    _RANKS: tuple[str, ...] = (
        "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
    )
    # The two red suits; every other legal suit is black.
    _RED_SUITS: tuple[str, ...] = ("hearts", "diamonds")

    def __init__(self, rank: str, suit: str) -> None:
        # Assigned directly rather than through the rank property, so that a
        # Card can still be built while the setter is unfinished. Note the
        # consequence, which is the lecture's warning about Account(-50):
        # __init__ bypasses the setter, so it performs no validation.
        self._rank: str = rank
        self._suit: str = suit

    def label(self) -> str:
        # A plain method, not a property: type(Card.label) is function,
        # while type(Card.rank) is property.
        return f"{self._rank} of {self._suit}"

    def __eq__(self, other: object) -> bool:
        # Given, so that the examples below can compare cards. Same concrete
        # type, same rank, same suit.
        return (
            type(self) is type(other)
            and self._rank == other._rank
            and self._suit == other._suit
        )

    @staticmethod
    def is_valid_rank(rank: str) -> bool:
        """Return True if `rank` is one of the 13 legal ranks, False otherwise.

        A @staticmethod because the question is about a rank, not about any
        particular card: it needs neither self nor cls. Callable either as
        Card.is_valid_rank(...) or on an instance.
        """
        raise NotImplementedError("replace this line with your implementation")

    @property
    def rank(self) -> str:
        """Return this card's rank.

        Decorated with @property, so `a_card.rank` runs this method while the
        call site still looks like a plain attribute.
        """
        raise NotImplementedError("replace this line with your implementation")

    @rank.setter
    def rank(self, value: str) -> None:
        """Set this card's rank, rejecting anything that is not one of the 13
        legal ranks by raising ValueError.

        The setter is where the check lives: a plain attribute would accept
        anything at all. Reuse is_valid_rank rather than repeating the list.
        """
        raise NotImplementedError("replace this line with your implementation")

    @property
    def color(self) -> str:
        """Return "red" for a card in a red suit, "black" otherwise.

        Computed rather than stored, and read-only because there is no
        matching setter: the color follows from the suit, so keeping a
        separate copy would only give it a way to go stale.
        """
        raise NotImplementedError("replace this line with your implementation")

    def __repr__(self) -> str:
        """Return a string that rebuilds this card, e.g. `Card('7', 'hearts')`.

        Note the quotes around the values. Use an f-string with !r, which asks
        for each value's own repr and supplies the quotes for you; building
        the string by plain concatenation would leave them out and produce
        `Card(7, hearts)`, which is not code that rebuilds anything.
        """
        raise NotImplementedError("replace this line with your implementation")


def announce(func):
    """Wrap `func` so that every call prints `calling <name>` before running,
    then returns whatever the wrapped function returns.

    Name the inner function `wrapper`, as in class. This one has no type
    annotations, and is the single exception to the annotation requirement:
    annotating it needs Callable, and this assignment allows no imports.
    """
    raise NotImplementedError("replace this line with your implementation")


class BoundedArray(DynamicArray):
    """A DynamicArray that refuses to hold more than a fixed number of
    values, however much room the underlying array happens to have.
    """

    # The most values a BoundedArray accepts unless told otherwise.
    _DEFAULT_LIMIT: int = 6

    def __init__(self, limit: int = _DEFAULT_LIMIT) -> None:
        """Set up a bounded array holding at most `limit` values.

        Call super().__init__() and let DynamicArray set up the underlying
        array, the capacity and the size -- do not repeat that work here.
        Then store the limit in an attribute whose name begins with TWO
        leading underscores.

        Keep the parameter optional. Inherited code creates new instances by
        calling cls() with no arguments, and that has to keep working.
        """
        raise NotImplementedError("replace this line with your implementation")

    def get_limit(self) -> int:
        """Return the greatest number of values this array will hold."""
        raise NotImplementedError("replace this line with your implementation")

    def add(self, value: int) -> None:
        """Store `value`, or raise IndexError("array is full") if this array
        already holds its limit.

        This overrides DynamicArray.add. Check the limit first, then hand
        the actual storing to the parent with super().add(value) rather than
        repeating the logic it already has.
        """
        raise NotImplementedError("replace this line with your implementation")


if __name__ == "__main__":
    # ----- Problem 1 -----
    da = DynamicArray()
    da.add(10001)
    da.add(60626)
    da.add(90210)
    print(da)                     # expected: [10001, 60626, 90210]
    print(len(da), da.get_size(), da.get_capacity())   # expected: 3 3 4

    print(da.get(0), da.get(2))   # expected: 10001 90210
    print(da.get(-1), da.get(3), da.get(100))          # expected: -1 -1 -1

    print(da.index_of(10001), da.index_of(90210), da.index_of(99999))
    # expected: 0 2 -1
    print(da.contains(60626), da.contains(99999))      # expected: True False

    da.add(11111)
    da.add(22222)
    print(da)                     # expected: [10001, 60626, 90210, 11111, 22222]
    print(len(da), da.get_capacity())                  # expected: 5 8

    print(da.remove(90210))       # expected: True
    print(da)                     # expected: [10001, 60626, 11111, 22222]
    print(len(da), da.get_capacity())                  # expected: 4 8
    print(da.remove(90210))       # expected: False
    print(da.index_of(22222))     # expected: 3

    # ----- Problem 2 -----
    a = DynamicArray.from_values([10001, 60626, 90210])
    print(a)                          # expected: [10001, 60626, 90210]
    print(len(a), a.get_capacity())   # expected: 3 4

    print(repr(a))
    # expected: DynamicArray.from_values([10001, 60626, 90210])
    print(repr(DynamicArray()))       # expected: DynamicArray.from_values([])

    b = DynamicArray.from_values([10001, 60626, 90210])
    print(a == b)                     # expected: True
    print(a is b)                     # expected: False

    # Same values, very different capacity -- still equal.
    wide = DynamicArray(64)
    wide.add(10001)
    wide.add(60626)
    wide.add(90210)
    print(a == wide, a.get_capacity(), wide.get_capacity())   # expected: True 4 64

    print(a == DynamicArray.from_values([10001, 60626]))         # expected: False
    print(a == DynamicArray.from_values([90210, 60626, 10001]))  # expected: False
    print(a == "not an array")        # expected: False
    print(a == None)                  # expected: False

    c = a + DynamicArray.from_values([11111, 22222])
    print(c)                          # expected: [10001, 60626, 90210, 11111, 22222]
    print(len(c))                     # expected: 5
    print(a)                          # expected: [10001, 60626, 90210]  (unchanged)
    print(len(a))                     # expected: 3  (unchanged)

    empty = DynamicArray()
    print(empty + empty)              # expected: []
    print(a + empty == a)             # expected: True

    # ----- Problem 3 -----
    card = Card("7", "hearts")

    print(card.label())                    # expected: 7 of hearts
    print(card.rank)                       # expected: 7
    print(card.color)                      # expected: red
    print(Card("K", "spades").color)       # expected: black

    print(Card.is_valid_rank("Q"))         # expected: True
    print(Card.is_valid_rank("1"))         # expected: False
    print(card.is_valid_rank("10"))        # expected: True

    print(repr(card))                      # expected: Card('7', 'hearts')
    print([card, card])
    # expected: [Card('7', 'hearts'), Card('7', 'hearts')]

    # The text of the repr is the code that rebuilds the card: typing it back
    # in by hand produces an equal Card. Shown this way rather than with
    # eval(), which runs whatever string it is handed and has no place in
    # ordinary code.
    print(Card("7", "hearts") == card)     # expected: True

    # The setter validates; the getter just reads.
    card.rank = "K"
    print(card.rank, card.label())         # expected: K K of hearts

    try:
        card.rank = "1"
    except ValueError as error:
        print("ValueError:", error)
        # expected: ValueError: '1' is not one of the 13 legal ranks

    # color has a getter and no setter, so it is read-only. Assigning to it
    # on purpose here, to show what that means. ty is right to object, so the
    # line carries ty's own ignore directive. Use that spelling: mypy's
    # equivalent comment is written differently, and ty reads it as a
    # malformed directive and warns about it.
    try:
        card.color = "green"  # ty: ignore[invalid-assignment]
    except AttributeError:
        print("AttributeError as expected")
        # expected: AttributeError as expected


    # ----- Problem 4 -----
    bounded = BoundedArray()
    print(type(bounded).__name__, bounded.get_limit())   # expected: BoundedArray 6

    for value in range(6):
        bounded.add(value)
    print(len(bounded), bounded.get_capacity())          # expected: 6 8

    # The override refuses the seventh value; the parent would have resized.
    # Capacity is 8 here and the limit is 6: room in the array is not
    # permission to use it.
    try:
        bounded.add(99)
    except IndexError as error:
        print("IndexError:", error)
        # expected: IndexError: array is full

    # Inherited from Problem 2, and still returning the right class, because
    # from_values builds with cls() rather than with DynamicArray().
    pair = BoundedArray.from_values([1, 2])
    print(type(pair).__name__, pair)                     # expected: BoundedArray [1, 2]
    print(repr(pair))                                    # expected: BoundedArray.from_values([1, 2])

    # from_values calls add, so the subclass's limit is enforced through it.
    try:
        BoundedArray.from_values([0, 1, 2, 3, 4, 5, 6])
    except IndexError as error:
        print("IndexError:", error)
        # expected: IndexError: array is full

    # Same values, different class: not equal.
    print(pair == DynamicArray.from_values([1, 2]))      # expected: False
    print(pair == BoundedArray.from_values([1, 2]))      # expected: True

    # Name mangling, in the open. Nothing is hidden -- the attribute is
    # simply filed under a rewritten key.
    print(sorted(vars(bounded)))
    # expected: ['_BoundedArray__limit', '_capacity', '_size', '_underlying']

    # ----- Problem 3, continued: applying the decorator -----
    #
    # Kept last on purpose. Decorating describe adds a printed line, so if
    # this block sat higher up, forgetting the decorator would shift every
    # line below it and make the other problems look wrong too.
    # A decorator rebinds the name to the wrapper. Defined here, inside the
    # main guard, so that importing this file never runs it.
    #
    # TODO: add the line `@announce` on its own, directly above the `def
    # describe` line below, so that describe is decorated. This is the one
    # place in this file where you ADD a line rather than replacing a
    # NotImplementedError, and the two prints that follow only produce the
    # output shown once that line is there.
    def describe(rank: str, suit: str) -> str:
        return f"{rank} of {suit}"

    print(describe("7", "hearts"))
    # expected: calling describe
    # expected: 7 of hearts
    print(describe.__name__)               # expected: wrapper
