# COMP 271 -- Week 06 assignment.
#
# Problem 1: Index-based recursion inside DynamicArray.
# Problem 2: Peel one piece per call.
# Problem 3: Divide and conquer.
# Problem 4: Recursive binary search for the first match.
#
# Everything below is complete except the six functions and methods whose
# body is a single `raise NotImplementedError(...)` line. Replace each of
# those lines with your implementation -- the raise is a placeholder, and any
# function still holding one counts as unanswered.
#
# Do not modify any other code, and do not rename anything.
# Run this file (uv run week06.py) to check your work against the expected
# output written beside each print below.

# Named constants, in the style of the Recursion II deck.
BASE: int = 10  # peel the last decimal digit: n % BASE, n // BASE
SPLIT_PARTS: int = 2  # halves per split


class DynamicArray:
    """A fixed-capacity array of non-negative integers that doubles its
    capacity whenever it fills up.
    """

    _DEFAULT_CAPACITY: int = 4
    _GROWTH_FACTOR: int = 2
    _EMPTY: int = -1  # sentinel: "this slot holds no value"

    def __init__(self, capacity: int = _DEFAULT_CAPACITY) -> None:
        # A capacity below 1 would leave nowhere to put the first value.
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity: int = capacity
        self._size: int = 0
        # Every slot starts as the sentinel.
        self._underlying: list[int] = []
        for _ in range(self._capacity):
            self._underlying.append(self._EMPTY)

    @classmethod
    def from_values(cls, values: list[int]) -> "DynamicArray":
        """Build a new array holding `values`, in order."""
        result = cls()
        for value in values:
            result.add(value)
        return result

    def __str__(self) -> str:
        # Show only the filled slots -- sentinel slots are internal detail.
        inside = ""
        for i in range(self._size):
            inside = inside + str(self._underlying[i])
            if i < self._size - 1:
                inside = inside + ", "
        return "[" + inside + "]"

    def __len__(self) -> int:
        """Return the number of values stored."""
        return self._size

    def get_capacity(self) -> int:
        """Return the total number of slots, sentinels included."""
        return self._capacity

    def resize(self) -> None:
        # Build a bigger array, copy what is real, then swap it in.
        bigger_capacity = self._capacity * self._GROWTH_FACTOR
        temp: list[int] = []
        for _ in range(bigger_capacity):
            temp.append(self._EMPTY)
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
        self._underlying[self._size] = value
        self._size = self._size + 1

    # ----- Problem 1: index-based recursion -----

    def reverse_between(self, lo: int, hi: int) -> None:
        """Reverse the stored values at positions lo through hi (both
        included), in place.

        Nothing is returned: the array itself changes. If lo > hi the range
        is empty and nothing happens. A non-empty range that reaches outside
        positions 0 through len(self) - 1 raises IndexError, so the sentinel
        slots past the end are never touched.
        """
        raise NotImplementedError("replace this line with your implementation")

    def reverse(self) -> None:
        """Given: reverse every stored value."""
        self.reverse_between(0, len(self) - 1)

    def count_matches_from(self, value: int, start: int) -> int:
        """Return how many of the stored values at positions start through
        len(self) - 1 equal `value`.

        A start at or past len(self) leaves nothing to count, so the answer
        is 0. A negative start raises IndexError. Only stored values count:
        the sentinel slots never do, even when `value` is -1.
        """
        raise NotImplementedError("replace this line with your implementation")

    def count(self, value: int) -> int:
        """Given: count every stored copy of `value`."""
        return self.count_matches_from(value, 0)


# ----- Problem 2: peel one piece per call -----


def digits_ascending(n: int) -> bool:
    """Return True if every decimal digit of n is at most the digit to its
    right.

    Equal neighbors are fine: 1223 gives True, 1323 gives False. A single
    digit gives True. A negative n raises ValueError. Work with the digits
    through n % BASE and n // BASE; do not convert n to a string.
    """
    raise NotImplementedError("replace this line with your implementation")


def collapse(text: str) -> str:
    """Return text with every run of repeated adjacent characters cut down
    to one: "aabccca" gives "abca".
    """
    raise NotImplementedError("replace this line with your implementation")


# ----- Problem 3: divide and conquer -----


def is_sorted(values: list[int]) -> bool:
    """Return True if values is in non-decreasing order (each item at most
    the next).

    Divide and conquer: split at the midpoint, check each half, then
    combine the two answers. Do not change `values`.
    """
    raise NotImplementedError("replace this line with your implementation")


# ----- Problem 4: first match by binary search -----


def first_index_between(nums: list[int], target: int, lo: int, hi: int) -> int:
    """Return the smallest index i with lo <= i <= hi and nums[i] == target,
    or -1 if there is none.

    nums is sorted in non-decreasing order and may hold repeats. Callers
    guarantee 0 <= lo and hi < len(nums), or lo > hi (an empty range).
    Halve the range on every call, as find did in class. Do not change
    `nums`.
    """
    raise NotImplementedError("replace this line with your implementation")


def find_first(nums: list[int], target: int) -> int:
    """Given: search the whole list."""
    return first_index_between(nums, target, 0, len(nums) - 1)


if __name__ == "__main__":
    # Each problem's checks run on their own, so you can work in any order:
    # an unfinished or crashing problem prints one line and the rest still run.

    def problem_1() -> None:
        # ----- Problem 1 -----
        a = DynamicArray.from_values([10, 20, 30, 40, 50])
        print(a, len(a), a.get_capacity())      # expected: [10, 20, 30, 40, 50] 5 8
        a.reverse_between(1, 3)
        print(a)                                # expected: [10, 40, 30, 20, 50]
        a.reverse()
        print(a)                                # expected: [50, 20, 30, 40, 10]
        # Peeking at a private attribute, only to show the sentinels stay put.
        # Code outside the class should not do this.
        print(a._underlying)                    # expected: [50, 20, 30, 40, 10, -1, -1, -1]
        a.reverse_between(2, 2)
        print(a)                                # expected: [50, 20, 30, 40, 10]
        # reverse_between changes the array itself: a second name sees it too.
        same = a
        a.reverse()
        print(same)                             # expected: [10, 40, 30, 20, 50]

        b = DynamicArray.from_values([7, 3, 7, 7, 1])
        print(b.count(7), b.count_matches_from(7, 1), b.count_matches_from(7, 4))   # expected: 3 2 0
        print(b.count_matches_from(7, 5), b.count(-1))  # expected: 0 0
        empty = DynamicArray()
        empty.reverse()
        print(empty, empty.count(0))            # expected: [] 0

    def problem_2() -> None:
        # ----- Problem 2 -----
        print(digits_ascending(1223), digits_ascending(1323), digits_ascending(7))
        # expected: True False True
        print(digits_ascending(0), digits_ascending(10), digits_ascending(59))
        # expected: True False True
        print(collapse("aabccca"), collapse("mississippi"))   # expected: abca misisipi
        print(repr(collapse("")), collapse("zzzz"))            # expected: '' z

    def problem_3() -> None:
        # ----- Problem 3 -----
        print(is_sorted([2, 5, 5, 8]), is_sorted([]), is_sorted([7]))
        # expected: True True True
        print(is_sorted([1, 3, 2, 4]), is_sorted([1, 2, 5, 3, 4, 6]))
        # expected: False False
        # Too deep to peel one item per call: only halving gets through.
        print(is_sorted(list(range(5_000))))    # expected: True

    def problem_4() -> None:
        # ----- Problem 4 -----
        nums = [2, 5, 5, 5, 8, 12, 12, 23]
        print(find_first(nums, 5), find_first(nums, 12), find_first(nums, 2))
        # expected: 1 5 0
        print(find_first(nums, 7), find_first(nums, 99), find_first([], 5))
        # expected: -1 -1 -1
        print(first_index_between(nums, 5, 2, 7), first_index_between(nums, 5, 4, 7))
        # expected: 2 -1
        print(find_first([4] * 100_000, 4))     # expected: 0
        print(find_first(list(range(100_000)), 99_999))   # expected: 99999

    for check in (problem_1, problem_2, problem_3, problem_4):
        try:
            check()
        except NotImplementedError:
            print(f"{check.__name__}: not finished yet, skipped")
        except Exception as error:  # noqa: BLE001 -- report any crash, keep going
            print(f"{check.__name__}: stopped by {type(error).__name__}: {error}")
