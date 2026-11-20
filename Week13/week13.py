# COMP 271 -- Week 13 assignment: hash tables, sorting and Big O.
#
# Problem 1: The Rider Directory (poly_hash, ChainedTable.put, ChainedTable.get).
# Problem 2: The Bike Dock (ProbingTable.put, ProbingTable._resize,
#            ProbingTable.longest_run).
# Problem 3: Busiest Stations (insertion_sort, rank_stations).
# Problem 4: Make It Linear (has_pair).
#
# Everything below is complete except the nine functions and methods whose
# body is a single `raise NotImplementedError(...)` line. Replace each of
# those lines with your implementation: the raise is a placeholder, and any
# function still holding one counts as unanswered.
#
# Do not modify any other code, and do not rename anything.
# Run this file (uv run week13.py) to check your work against the expected
# output written beside each print below.

BASE: int = 31                  # weight per character position (Day 23)
GROWTH_FACTOR: int = 2          # a full table grows to about twice its slots
SMALLEST_PRIME: int = 2         # the first prime


def _is_prime(n: int) -> bool:
    """Given: return True when n is a prime number."""
    prime = n >= SMALLEST_PRIME
    divisor = SMALLEST_PRIME
    # Try every divisor up to the square root of n
    while prime and divisor * divisor <= n:
        prime = n % divisor != 0
        divisor += 1
    return prime


def next_prime(n: int) -> int:
    """Given: return the smallest prime that is at least n."""
    candidate = n
    # Step up one number at a time until a prime turns up
    while not _is_prime(candidate):
        candidate += 1
    return candidate


# ----- Problem 1 -----

CHAIN_START: int = 11           # slots in a new ChainedTable
MAX_CHAIN_LOAD: float = 1.0     # a ChainedTable grows once alpha passes this

Chain = list[tuple[str, int]]   # one slot's (key, value) pairs, oldest first


def poly_hash(word: str, slot_count: int) -> int:
    """Return the slot for word in a table of slot_count slots.

    Start a total at 0. For each character, multiply the total by BASE and
    add the character's code, ord(char). Return the total's remainder when
    divided by slot_count. An empty word has total 0.
    """
    raise NotImplementedError("replace this line with your implementation")


class ChainedTable:
    """A hash table from station or rider names (str) to counts (int).

    Each slot holds a chain: a list of (key, value) pairs. A key's slot is
    poly_hash(key, number of slots).
    """

    def __init__(self) -> None:
        # One empty chain per slot
        self._slots: list[Chain] = [[] for _ in range(CHAIN_START)]
        # How many different keys the table holds
        self._size: int = 0

    def size(self) -> int:
        """Return the number of keys stored."""
        return self._size

    def slot_count(self) -> int:
        """Return the number of slots (chains)."""
        return len(self._slots)

    def load_factor(self) -> float:
        """Return alpha = keys stored / slots."""
        return self._size / len(self._slots)

    def _grow(self) -> None:
        """Given: move every pair into next_prime(GROWTH_FACTOR * slots) chains.

        Old chains are emptied in slot order 0, 1, 2, ..., each from its
        oldest pair to its newest, and every key is hashed again with the
        new number of slots.
        """
        old_slots = self._slots
        new_count = next_prime(GROWTH_FACTOR * len(old_slots))
        self._slots = [[] for _ in range(new_count)]
        # Rehash: a key's slot depends on the number of slots
        for chain in old_slots:
            for key, value in chain:
                self._slots[poly_hash(key, new_count)].append((key, value))

    def put(self, key: str, value: int) -> None:
        """Store value under key.

        If key is already in its chain, replace that pair's value in place.
        Otherwise append (key, value) to the end of the chain and count the
        new key. Then, if the load factor has passed MAX_CHAIN_LOAD, call
        self._grow() once.
        """
        raise NotImplementedError("replace this line with your implementation")

    def get(self, key: str) -> int | None:
        """Return the value stored under key, or None if key is not stored.

        Look only in key's own chain.
        """
        raise NotImplementedError("replace this line with your implementation")


# ----- Problem 2 -----

PROBE_START: int = 7            # slots in a new ProbingTable
MAX_PROBE_LOAD: float = 0.7     # a ProbingTable grows once alpha passes this


class ProbingTable:
    """A linear-probing hash table from bike numbers (int) to docks (str).

    _keys[i] is the bike stored in slot i (None means empty) and _values[i]
    its dock. A bike's home slot is key % number of slots.
    """

    def __init__(self) -> None:
        # Two parallel lists, all slots empty
        self._keys: list[int | None] = [None] * PROBE_START
        self._values: list[str | None] = [None] * PROBE_START
        # How many bikes the table holds
        self._size: int = 0

    def size(self) -> int:
        """Return the number of bikes stored."""
        return self._size

    def slot_count(self) -> int:
        """Return the number of slots."""
        return len(self._keys)

    def load_factor(self) -> float:
        """Return alpha = bikes stored / slots."""
        return self._size / len(self._keys)

    def slots(self) -> list[int | None]:
        """Return a copy of _keys, to print the table's layout."""
        return list(self._keys)

    def _find_slot(self, key: int) -> int:
        """Given: return the slot holding key, or the empty slot where the
        walk from key's home slot ends (linear probing, wrapping to 0)."""
        slot = key % len(self._keys)
        # Walk past slots that hold other keys
        while self._keys[slot] is not None and self._keys[slot] != key:
            slot = (slot + 1) % len(self._keys)
        return slot

    def get(self, key: int) -> str | None:
        """Given: return the dock stored for key, or None if key is missing."""
        return self._values[self._find_slot(key)]

    def put(self, key: int, value: str) -> None:
        """Store value under key with linear probing.

        Find key's slot with self._find_slot. If that slot is empty, the key
        is new: count it. Write the key and value there (an existing key
        keeps its slot and gets the new value). Then, if the load factor has
        passed MAX_PROBE_LOAD, call self._resize() once.
        """
        raise NotImplementedError("replace this line with your implementation")

    def _resize(self) -> None:
        """Grow to next_prime(GROWTH_FACTOR * old slot count) empty slots,
        then place every stored key again.

        Visit the old slots in order 0, 1, 2, ... and place each key with
        its value in the new table, using self._find_slot (do not call put).
        The number of keys stored does not change.
        """
        raise NotImplementedError("replace this line with your implementation")

    def checks(self, key: int) -> int:
        """Given: return how many slots a lookup of key checks.

        The same walk as _find_slot, counting every slot looked at: the home
        slot, each slot holding another key, and the last slot (the one
        holding key, or the empty slot that ends a miss).
        """
        slot = key % len(self._keys)
        count = 1
        # Same walk as _find_slot, counting every step
        while self._keys[slot] is not None and self._keys[slot] != key:
            slot = (slot + 1) % len(self._keys)
            count += 1
        return count

    def longest_run(self) -> int:
        """Return the length of the longest run: the most full slots in a
        row, where a run may wrap from the last slot around to slot 0.

        An empty table returns 0; a table with every slot full returns the
        number of slots. Change nothing.
        """
        raise NotImplementedError("replace this line with your implementation")


# ----- Problem 3 -----


def insertion_sort(names: list[str]) -> None:
    """Sort names into alphabetical order, in place, with insertion sort.

    For i from 1 up, take names[i], shift each bigger name before it one
    slot right, and drop it into the gap.
    """
    raise NotImplementedError("replace this line with your implementation")


def rank_stations(rides: list[str]) -> list[str]:
    """Return every station in rides once, the most rides first.

    Each entry of rides is the station one ride started from. Stations with
    the same number of rides come out in alphabetical order.

    Count each station's rides in a ChainedTable. Then bucket sort by
    count: bucket c holds the stations with exactly c rides. Sort each
    bucket with insertion_sort, then gather from the biggest count down.
    """
    raise NotImplementedError("replace this line with your implementation")


# ----- Problem 4 -----


def has_pair_slow(minutes: list[int], target: int) -> bool:
    """Given: return True when two different rides' minutes add up to target."""
    found = False
    # Try every ride with every later ride
    for i in range(len(minutes)):
        for j in range(i + 1, len(minutes)):
            if minutes[i] + minutes[j] == target:
                found = True
    return found


def has_pair(minutes: list[int], target: int) -> bool:
    """Return True when two different rides' minutes add up to target.

    Same answer as has_pair_slow, in Theta(n) time on average: walk the
    list once, keeping the minutes seen so far in a set.
    """
    raise NotImplementedError("replace this line with your implementation")


if __name__ == "__main__":
    # Each problem's checks run on their own, so you can work in any order:
    # an unfinished or crashing problem prints one line and the rest still run.

    def problem_1() -> None:
        # ----- Problem 1 -----
        # The first two match the Coat Check handout, the next three Day 23.
        print(poly_hash("ab", 8), poly_hash("ba", 8), poly_hash("", 11))
        # expected: 1 7 0
        print(poly_hash("stop", 11), poly_hash("pots", 11), poly_hash("tops", 11))
        # expected: 6 3 1
        riders = ChainedTable()
        for name in ["ana", "ben", "cy", "dee"]:
            riders.put(name, len(name))
        riders.put("ben", 9)
        print(riders.get("ben"), riders.get("cy"), riders.get("zoe"), riders.size())
        # expected: 9 2 None 4
        for name in ["eli", "fay", "gus", "hal", "ida", "jo", "kai"]:
            riders.put(name, 1)
        print(riders.size(), riders.slot_count())       # expected: 11 11
        riders.put("lu", 1)
        print(riders.size(), riders.slot_count(), riders.get("ana"))
        # expected: 12 23 3

    def problem_2() -> None:
        # ----- Problem 2 -----
        # The same bikes and table sizes as the Moving Day handout.
        dock = ProbingTable()
        for bike in [14, 42, 31, 15]:
            dock.put(bike, "Cudahy")
        print(dock.slots())
        # expected: [14, 42, 15, 31, None, None, None]
        print(dock.longest_run(), ProbingTable().longest_run())    # expected: 4 0
        dock.put(50, "Damen")
        print(dock.slot_count(), dock.size(), dock.longest_run())   # expected: 17 5 4
        print(dock.slots())
        # expected: [50, None, None, None, None, None, None, None, 42, None, None, None, None, None, 14, 15, 31]
        dock.put(33, "Halas")
        dock.put(42, "Piper")
        print(dock.get(33), dock.get(42), dock.get(99), dock.size())
        # expected: Halas Piper None 6
        print(dock.longest_run(), dock.checks(48))       # expected: 5 6

    def problem_3() -> None:
        # ----- Problem 3 -----
        names = ["Piper", "Damen", "Halas", "Cudahy"]
        insertion_sort(names)
        print(names)                    # expected: ['Cudahy', 'Damen', 'Halas', 'Piper']
        rides = ["Halas", "Damen", "Piper", "Damen", "Cudahy", "Halas",
                 "Damen", "Mundelein", "Piper"]
        print(rank_stations(rides))
        # expected: ['Damen', 'Halas', 'Piper', 'Cudahy', 'Mundelein']
        print(rank_stations([]), rank_stations(["Halas"]))
        # expected: [] ['Halas']

    def problem_4() -> None:
        # ----- Problem 4 -----
        minutes = [12, 30, 7, 25, 18]
        print(has_pair_slow(minutes, 37), has_pair(minutes, 37), has_pair(minutes, 50))
        # expected: True True False
        print(has_pair([25], 50), has_pair([25, 25], 50), has_pair([], 0))
        # expected: False True False
        evens = list(range(0, 400_000, 2))      # far too slow for the slow version
        print(has_pair(evens, 3), has_pair(evens, 399_996))
        # expected: False True

    for check in (problem_1, problem_2, problem_3, problem_4):
        try:
            check()
        except NotImplementedError:
            print(f"{check.__name__}: not finished yet, skipped")
        except Exception as error:  # noqa: BLE001 -- report any crash, keep going
            print(f"{check.__name__}: stopped by {type(error).__name__}: {error}")
