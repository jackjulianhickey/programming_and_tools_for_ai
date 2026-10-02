"""Composition. Go and find a collision. SOLUTION.

Run the tests:

    python -m doctest W04_Solutions/E04_string_collision.py

No output means every test passed.

With integers a collision is easy to arrange: 3 and 11 land in the same
bucket of 8, every time. Strings are harder, because you cannot predict where
one lands -- so you have to search.

Python scrambles string hashing differently every time it starts, so
hash("cat") is a different number in each run and "cat" lands in a different
bucket. Run this file twice as a program and you will get a different pair.
That is why the doctests below check that the pair collides, rather than
naming the two words.
"""

# Given: E02's one-liner, so this file stands alone.
def bucket_index(key, capacity):
    return hash(key) % capacity


def find_collision(words, capacity):
    """Return two different words from `words` sharing a bucket, or None.

    Walk the words, remembering which bucket each one landed in. The first
    time a bucket comes up twice, you have found your pair. Return it as
    (first_word, second_word), in the order you met them.

    Twelve words cannot fit in eight buckets without sharing one, so this
    always finds something -- though *which* pair it finds varies from run
    to run:

    >>> words = ["cat", "dog", "emu", "fox", "owl", "pig",
    ...          "rat", "yak", "ant", "bee", "cow", "elk"]
    >>> pair = find_collision(words, 8)
    >>> pair is None
    False
    >>> first, second = pair
    >>> first != second
    True
    >>> bucket_index(first, 8) == bucket_index(second, 8)
    True

    With more buckets than words there may be no collision at all, so the
    answer can honestly be None:

    >>> find_collision(["cat"], 8) is None
    True
    >>> find_collision([], 8) is None
    True
    """
    seen = {}
    for word in words:
        i = bucket_index(word, capacity)
        if i in seen:
            return (seen[i], word)
        seen[i] = word
    return None


if __name__ == "__main__":
    words = ["cat", "dog", "emu", "fox", "owl", "pig",
             "rat", "yak", "ant", "bee", "cow", "elk"]
    pair = find_collision(words, 8)
    print(f"collision: {pair[0]!r} and {pair[1]!r} both go in bucket "
          f"{bucket_index(pair[0], 8)}")
    # With far more buckets than words, a collision becomes very unlikely.
    print(f"with ten million buckets: {find_collision(words, 10_000_000)}")
