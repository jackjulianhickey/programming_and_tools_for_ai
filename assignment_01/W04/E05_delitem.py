"""Composition. Finish the data model: make `del d[k]` work.

Run the tests:

    python -m doctest W04/E05_delitem.py

No output means every test passed.

SimpleDict is given below with one method missing. `del d[k]` calls
`__delitem__`, one more row in the data model table; without it, Python
raises TypeError.

Hint: `del` also removes an element from a list, eg:
>>> L = ['a', 'b', 'c']
>>> del L[0]
>>> L
['b', 'c']
"""


# Given: SimpleDict from E01, unchanged, with the method docstrings removed
# for brevity -- you have read them there.
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
        """Make `del d[key]` work. Raise KeyError if the key is not there.

        Find the pair in its bucket, exactly as `__getitem__` does, then
        remove it from that bucket's list and drop the count by one.

        >>> d = SimpleDict()
        >>> d["cat"] = 4
        >>> d["dog"] = 9
        >>> del d["cat"]
        >>> len(d)
        1
        >>> "cat" in d
        False
        >>> d["dog"]
        9

        Deleting something that is not there is an error, as it is for a real
        dict -- silently doing nothing would hide the bug:

        >>> del d["emu"]
        Traceback (most recent call last):
            ...
        KeyError: 'emu'

        The key can be added again afterwards, and the count is right:

        >>> d["cat"] = 100
        >>> sorted(d.items())
        [('cat', 100), ('dog', 9)]
        >>> len(d)
        2

        Deleting the collided key leaves the other one findable. Recall that
        3 and 11 share a bucket when there are 8:

        >>> d = SimpleDict(capacity=8)
        >>> d[3], d[11] = "three", "eleven"
        >>> del d[3]
        >>> d[11]
        'eleven'
        >>> 3 in d
        False
        """
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.n -= 1
                return
        raise KeyError(key)


# Deleting is easy here only because each bucket is its own list: take the
# pair out, and the bucket closes up behind it. Hash tables that store one
# pair per slot and step along to the next free slot on a collision -- "open
# addressing", which is what real CPython dicts use -- cannot do this. Removing
# a pair there would break the chain of slots that a later key was found
# through, so they must leave a marker behind saying "something was deleted
# here, keep looking". Those markers accumulate, and the table has to be
# rebuilt to clear them. Our slower design is much easier to delete from.
