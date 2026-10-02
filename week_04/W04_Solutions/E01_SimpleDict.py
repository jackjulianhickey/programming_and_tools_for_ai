"""Drill. You don't need to write anything, just run this file. SOLUTION.

This file contains two classes discussed in the lecture: 
* PairListDict (easy to write but inefficient) and 
* SimpleDict (more complicated but quite efficient for a Python implementation)

To run tests:

    python -m doctest W04_Solutions/E01_SimpleDict.py

(Remember, if there is no output, everything passed.)

To run the file as a program, which will run the timing tests:

    python W04_Solutions/E01_SimpleDict.py

"""

import random
import string
import time


class PairListDict:
    """A dictionary stored as list of (key, value) pairs (ie, not a hashmap)

    >>> d = PairListDict()
    >>> d["cat"] = 4
    >>> d["dog"] = 4
    >>> d["cat"]
    4
    >>> len(d)
    2

    Writing an existing key replaces the old value:

    >>> d["cat"] = 9
    >>> d["cat"], len(d)
    (9, 2)

    We can do a for-loop and check `in`, thanks to __iter__:
    >>> for k in d: print(k)
    cat
    dog
    >>> "cat" in d
    True
    >>> "monkey" in d
    False

    Every lookup walks the list until it finds the key, so a dictionary of a
    million pairs could do a million comparisons to check whether the key is 
    present. In SimpleDict below we will fix this issue.
    """

    def __init__(self):
        self.pairs = [] # starts empty: no storage is wasted

    def __setitem__(self, key, value):
        for i, (k, v) in enumerate(self.pairs):
            if k == key: # the key exists, so overwrite its old value
                self.pairs[i] = (key, value) 
                return
        self.pairs.append((key, value)) # notice we store both key and value at idx i

    def __getitem__(self, key):
        for k, v in self.pairs:
            if k == key:
                return v
        raise KeyError(key) # remember, this is what a real Python dict does

    def __len__(self):
        return len(self.pairs)

    def __iter__(self):
        for k, v in self.pairs:
            yield k # a generator


class SimpleDict:
    """A dictionary using hashing. Every key goes to a specific bucket
    calculated as hash(k) % table_size. But if there is already
    a different key there (a *collision*), it's ok, each bucket stores
    a *list* of items. That list starts *empty*, of course.

    After adding lots of items, the dict becomes quite full and we get a
    lot of collisions, which makes it slow. We create a bigger list
    (bigger n, more wasted space), and because n has changed, every
    item's bucket has to be recalculated.

    It behaves like a real `dict` for everything we have used one for:

    >>> d = SimpleDict()
    >>> d["cat"] = 4
    >>> d["dog"] = 4
    >>> d["cat"]
    4
    >>> len(d)
    2
    >>> "cat" in d
    True
    >>> "emu" in d
    False
    >>> sorted(d) # notice we sort this output for doctest purposes, see below
    ['cat', 'dog']

    A missing key is a `KeyError`, the same as a real dict:

    >>> d["emu"]
    Traceback (most recent call last):
        ...
    KeyError: 'emu'

    Writing an existing key replaces its value:

    >>> d["cat"] = 9
    >>> d["cat"], len(d)
    (9, 2)

    Keys must be hashable, so a tuple works and a list does not:

    >>> d[(1, 2)] = "a point"
    >>> d[(1, 2)]
    'a point'
    >>> d[[1, 2]] = "a mistake"
    Traceback (most recent call last):
        ...
    TypeError: unhashable type: 'list'

    Aboev we used `sorted(d)`. because of some unimportant internal details, 
    `list(d)` could give "cat", "dog", or "dog", "cat". To ensure our doctest
    is deterministic, we sort.
    """

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.n = 0
        self.buckets = [[] for _ in range(capacity)] # we use a lot of space even for an empty dict

    def _bucket(self, key):
        """A key goes into a certain bucket.

        `hash` turns any hashable object into an int, and `%` maps that int
        into the range of bucket numbers we actually have.

        For any integer x, hash(x) == x. So it's easy to produce a hash collision:

        >>> d = SimpleDict(capacity=8)
        >>> hash(3)
        3
        >>> hash(11)
        11
        >>> hash(3) % 8
        3
        >>> hash(11) % 8 # hash collision
        3
        >>> d[3] = "three"
        >>> d[11] = "eleven"
        >>> d.buckets[3]
        [(3, 'three'), (11, 'eleven')]

        That is a **collision**. We solve it by storing both pairs in the same
        bucket using a list. Lookup has to scan that list.
        >>> d[11]
        'eleven'
        """
        return self.buckets[hash(key) % self.capacity]

    def __setitem__(self, key, value):
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value) # replace: not a new pair
                return
        bucket.append((key, value)) # append a new pair, and check capacity
        self.n += 1
        if self.n > 0.75 * self.capacity:
            self._grow()

    def __getitem__(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

    # There is no __contains__ here, on purpose. `key in d` still works,
    # because Python falls back on __iter__ and compares every key -- so it
    # works, and it is O(n), which throws away everything hashing bought us.
    # Writing the missing method is E06.

    def __len__(self):
        """Make `len(d)` work. We keep a running count rather than recount.

        >>> d = SimpleDict()
        >>> len(d)
        0
        >>> d["cat"] = 4
        >>> len(d)
        1
        """
        return self.n

    def __iter__(self):
        """Make `for k in d` work. A generator, as in Week 3.

        >>> d = SimpleDict()
        >>> d["cat"] = 4
        >>> d["dog"] = 9
        >>> sorted(d)
        ['cat', 'dog']
        >>> sorted(k for k in d)
        ['cat', 'dog']
        """
        for bucket in self.buckets:
            for k, v in bucket:
                yield k

    def items(self):
        """Every (key, value) pair, in bucket order.

        >>> d = SimpleDict()
        >>> d["cat"] = 4
        >>> sorted(d.items())
        [('cat', 4)]
        """
        for bucket in self.buckets:
            for pair in bucket:
                yield pair

    def __repr__(self):
        """What the REPL shows. Make it look like the thing it imitates.

        >>> SimpleDict()
        SimpleDict({})
        >>> d = SimpleDict()
        >>> d["cat"] = 4
        >>> d
        SimpleDict({'cat': 4})
        """
        inner = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"SimpleDict({{{inner}}})"

    def _grow(self):
        """Double the number of buckets and re-file every pair.

        We cannot just copy the buckets across. A pair's bucket number is
        `hash(key) % capacity`, and `capacity` has just changed, so almost
        everything belongs somewhere new. Re-inserting is the whole job:

        >>> d = SimpleDict(capacity=8)
        >>> for i in range(7):
        ...     d[i] = i * i
        >>> d.capacity                  # grew at the 7th, since 7 > 0.75 * 8
        16
        >>> len(d)                      # and lost nothing
        7
        >>> d[6]
        36

        The re-inserts cannot themselves trigger another grow: capacity has
        just doubled, so the load factor is now about 0.375.
        """
        pairs = list(self.items())
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.n = 0
        for k, v in pairs:
            self[k] = v


def random_words(n, seed=0):
    """n distinct-ish random 8-letter words, to fill a dictionary with."""
    r = random.Random(seed)
    return ["".join(r.choice(string.ascii_lowercase) for _ in range(8))
            for _ in range(n)]


PROBE = 200          # how many lookups we time, the same for every n
REPEATS = 5          # how many times we repeat the whole measurement


def time_lookups(make, n):
    """Microseconds per successful lookup, in a dictionary holding n keys.

    Timing is easy to get wrong, so note four things.
    """
    keys = random_words(n)

    # Fill the dictionary first. Building it is not what we are timing.
    d = make()
    for k in keys:
        d[k] = 1

    # 1. Time the same number of lookups for every n. If a small dictionary
    #    got fewer lookups, its row would carry more of the fixed cost of
    #    starting and stopping the clock, and would look slower than it is.
    #    The keys are spread through the dictionary rather than taken from the
    #    front, because PairListDict finds an early key much faster than a
    #    late one, and we want its average.
    probe = [keys[i * n // PROBE] for i in range(PROBE)]

    # 2. Every key we ask for is present. A *missing* key is a different
    #    measurement -- PairListDict has to scan the whole list to be sure --
    #    so mixing the two would average two different things.
    best = None
    for _ in range(REPEATS):
        start = time.perf_counter()
        for k in probe:
            d[k] # no printing inside a timing loop, as printing is far slower than computation
        elapsed = time.perf_counter() - start

        # 3. Keep the *fastest* run, not the average. Anything else happening
        #    on the machine can only make a run slower, never faster, so the
        #    smallest number is the one least polluted by the rest of the
        #    computer. This is what the standard `timeit` module recommends.
        if best is None or elapsed < best:
            best = elapsed

    # 4. Report time per lookup, in microseconds, so the numbers stay readable
    #    and the columns can be compared across rows.
    return best / len(probe) * 1e6


if __name__ == "__main__":
    # Warm up, and throw the answers away. The first measurements a fresh
    # Python process makes are always the slowest: the CPU is still at a low
    # clock speed, nothing is in cache, and CPython has not yet specialised the
    # bytecode of a loop it has only just met. Without this, every row is a
    # little faster than the one above it -- which looks exactly like a result,
    # and is not. Measure the same n four times in a row and you can watch it
    # happen.
    for _ in range(3):
        time_lookups(SimpleDict, 1000)

    print("microseconds per lookup\n")
    print(f"{'n':>7} | {'PairListDict':>13} | {'SimpleDict':>11} | {'real dict':>10}")
    for n in [100, 400, 1600, 6400]:
        row = [time_lookups(m, n) for m in (PairListDict, SimpleDict, dict)]
        print(f"{n:>7} | {row[0]:>13.2f} | {row[1]:>11.2f} | {row[2]:>10.2f}")

    # Read the table down a column, not across a row. Across a row we are
    # comparing three different programs, and the constant factors differ.
    # Down a column we are asking the only question that matters here: what
    # happens to this program when the problem gets bigger?
    print("\nfour times the keys costs PairListDict four times the time,")
    print("and costs SimpleDict nothing. That is O(n) against O(1).\n")

    # Why SimpleDict stays flat: growing keeps the buckets short no matter how
    # many keys there are, so a lookup always scans a list of about one item.
    d = SimpleDict()
    for k in random_words(1000):
        d[k] = 1
    lengths = [len(b) for b in d.buckets]
    print(f"SimpleDict holding {len(d)} keys: {d.capacity} buckets, "
          f"longest {max(lengths)}, mean {sum(lengths) / len(lengths):.2f}")
