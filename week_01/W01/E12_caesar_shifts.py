"""Extension. Breaking the cipher by brute force.

Run the tests:

    python -m doctest W01/E12_caesar_shifts.py

No output means every test passed.
"""

# Given: the cipher from the lecture. You do not need to change it.
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def caesar(s, k):
    """Shift every letter of s forward by k places. Leave other characters alone."""
    shifted = ALPHABET[k % 26:] + ALPHABET[:k % 26]
    out = []
    for c in s:
        if c in ALPHABET:
            out.append(shifted[ALPHABET.index(c)])
        else:
            out.append(c)
    return "".join(out)


def all_shifts(s):
    """Return every possible decoding of s, as a list of (k, plaintext) tuples.

    Entry k says: if the message was encoded with a shift of k, it reads
    like this. There are 26 possible shifts.

    >>> shifts = all_shifts("khoor")
    >>> len(shifts)
    26
    >>> shifts[0]
    (0, 'khoor')
    >>> shifts[3]
    (3, 'hello')
    >>> shifts[3][1]
    'hello'
    """
    list = []
    for k in range(26):
        list.append((k, caesar(s, (26-k)))) # mod is handled by caesar function
    return list

