"""Extension. Make `k in d` fast, and prove that you did.

Run the tests:

    python -m doctest W04/E06_fast_contains.py

No output means every test passed. Then run it as a program to get the table
you need for the answer at the bottom:

    python W04/E06_fast_contains.py

E01 left one method out of SimpleDict on purpose. `key in d` works anyway,
because Python falls back on `__iter__` and compares every key in turn -- so
SimpleDict does all the work of hashing and then throws the benefit away.

Your job is the four lines that use it. All the measuring is written for you.

QUESTION: run the program, paste its table into the comment at the bottom of
this file, and answer three things about it.

  1. The E01 column comes out no faster than PairListDict, and actually a
     little slower. Why, when E01 showed it hundreds of times faster at `d[k]`?
     Hint: our workload is `in`.
  2. Why does an absent key cost about twice what a present one costs, for the
     first two columns, but the same for the third?
  3. Which change made `in` fast -- hashing, or writing `__contains__`?
"""

import time

# E01's SimpleDict has no __contains__, so we keep it under another name and
# time it alongside the one below, which will have yours.
from E01_SimpleDict import PairListDict, random_words
from E01_SimpleDict import SimpleDict as SimpleDictNoContains


# Given: SimpleDict from E01, unchanged, and E05's __delitem__, with the method
# docstrings removed for brevity.
class SimpleDict:

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.n = 0
        self.buckets = [[] for _ in range(capacity)]

    def _bucket(self, key):
        return self.buckets[hash(key) % self.capacity]

    def __setitem__(self, key, value):
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.n += 1
        if self.n > 0.75 * self.capacity:
            self._grow()

    def __getitem__(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

    def __len__(self):
        return self.n

    def __iter__(self):
        for bucket in self.buckets:
            for k, v in bucket:
                yield k

    def items(self):
        for bucket in self.buckets:
            for pair in bucket:
                yield pair

    def __repr__(self):
        inner = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"SimpleDict({{{inner}}})"

    def _grow(self):
        pairs = list(self.items())
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.n = 0
        for k, v in pairs:
            self[k] = v

    def __delitem__(self, key):
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.n -= 1
                return
        raise KeyError(key)

    def __contains__(self, key):
        """Return whether `key` is in the dictionary, without scanning it all.

        The key can only ever be in one bucket, so there is no reason to look
        in any other. `self._bucket(key)` hands you that bucket, and it holds
        about one pair.

        >>> d = SimpleDict()
        >>> d["cat"] = 4
        >>> "cat" in d
        True
        >>> "emu" in d
        False

        An empty dictionary contains nothing, and must not fall over:

        >>> "cat" in SimpleDict()
        False

        It must still be right after the table has grown, and when two keys
        share a bucket (3 and 11 do, when there are 8):

        >>> d = SimpleDict(capacity=8)
        >>> for i in range(20):
        ...     d[i] = i
        >>> all(i in d for i in range(20))
        True
        >>> 20 in d, 3 in d, 11 in d
        (False, True, True)

        A deleted key must stop being found:

        >>> del d[3]
        >>> 3 in d, 11 in d
        (False, True)

        It must agree with the slow version it replaces, on every key:

        >>> slow = SimpleDictNoContains()
        >>> fast = SimpleDict()
        >>> for w in random_words(200):
        ...     slow[w] = fast[w] = 1
        >>> probe = random_words(200) + [w + "!" for w in random_words(50)]
        >>> all((p in slow) == (p in fast) for p in probe)
        True
        """
        bucket = self._bucket(key)
        for k, v in bucket:
            if k == key:
                return True
        return False


# Given: the measuring. You do not have to understand it, but the comments say
# why it is written this way -- timing is easy to get wrong, and a wrong
# measurement is worse than no measurement.
def time_in(d, probe, repeats=5):
    """Microseconds per `k in d`, over the keys in `probe`."""
    best = None
    for _ in range(repeats):
        start = time.perf_counter()
        for k in probe:
            k in d # hint: our workload is `in`
        elapsed = time.perf_counter() - start
        # Keep the fastest run: anything else happening on the computer can
        # only make a run slower, so the smallest number is the cleanest one.
        if best is None or elapsed < best:
            best = elapsed
    return best / len(probe) * 1e6


def columns():
    """The three dictionaries to compare, and the heading over each.

    A function rather than a list, so that this file still imports, and still
    reports its doctests, before you have written __contains__. The third
    column is headed by what we added rather than by the class name: that is
    question 3.
    """
    return [(PairListDict, "PairListDict"),
            (SimpleDictNoContains, "SimpleDict (E01)"),
            (SimpleDict, "+ __contains__")]


def row(n):
    """Time `in` on all three dictionaries, at size n, and print one row."""
    keys = random_words(n)
    # Spread the probe through the dictionary rather than taking the first 100.
    # PairListDict stores pairs in the order they arrived and searches from the
    # front, so the first 100 keys are the 100 it finds fastest -- probing those
    # would make it look O(1) when it is not.
    present = [keys[i * n // 100] for i in range(100)]
    absent = [k + "!" for k in present]      # 100 keys that are certainly not there
    out = []
    for cls, _ in columns():
        d = cls()
        for k in keys:
            d[k] = 1
        out.append(time_in(d, present))
        out.append(time_in(d, absent))
    print(f"{n:>6} |{out[0]:>8.1f}{out[1]:>8.1f} |{out[2]:>8.1f}{out[3]:>8.1f} |"
          f"{out[4]:>8.2f}{out[5]:>8.2f}")


if __name__ == "__main__":
    # Warm up and discard. The first measurements a fresh Python process makes
    # are always the slowest, and without this every row looks a little faster
    # than the one above it for no reason at all.
    for _ in range(3):
        time_in(SimpleDict(), ["x"] * 100)

    print("microseconds for `k in d`\n")
    print(f"{'':>6} |" + " |".join(f"{label:>16}" for _, label in columns()))
    print(f"{'n':>6} |{'present':>8}{'absent':>8} |{'present':>8}{'absent':>8} |"
          f"{'present':>8}{'absent':>8}")
    for n in (500, 2000, 8000):
        row(n)


# ANSWER: 
#        |    PairListDict |SimpleDict (E01) |  + __contains__
#      n | present  absent | present  absent | present  absent
#    500 |     7.6    14.3 |    22.4    45.6 |    0.29    0.28
#   2000 |    31.6    60.3 |    91.5   173.7 |    0.29    0.28
#   8000 |   125.3   234.1 |   375.0   689.2 |    0.29    0.28
