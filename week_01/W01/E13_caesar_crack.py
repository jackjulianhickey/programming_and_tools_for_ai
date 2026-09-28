"""Extension. Letting the computer pick the right decoding.

Run the tests:

    python -m doctest W01/E13_caesar_crack.py

No output means every test passed.

QUESTION: crack fails on the short message below. Why? What would you
need in order to fix it? Write your answer in the comment at the bottom.
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
    """Given: every possible decoding, as (k, plaintext) tuples."""
    return [(k, caesar(s, -k)) for k in range(26)]


def english_score(text):
    """Score how English-looking text is: count the commonest English letters.

    The six commonest letters in English are e, t, a, o, i, n. Count how
    many characters of text are one of those. Upper case counts too.

    >>> english_score("hello there")
    5
    >>> english_score("xyz")
    0
    >>> english_score("attack at dawn")
    8
    """
    count = 0
    for char in text:
        if char in "etaoin":
            count+=1
    return count


def crack(s):
    """Return the decoding of s that scores highest. No human required.

    >>> crack("wkh txlfn eurzq ira")
    'the quick brown fox'
    >>> crack("dvvk dv rk kyv sizuxv rk urne")
    'meet me at the bridge at dawn'
    >>> crack("ymj wfns ns xufns kfqqx rfnsqd ts ymj uqfns")
    'the rain in spain falls mainly on the plain'

    But it is only a guess, and on a short message it guesses wrong:

    >>> crack("khoor zruog")
    'ebiil tloia' # It fails because even though these are the most commonly used letters that does not a word garauntee. 
    """
    list = all_shifts(s)

    score = [] 
    for i in range(26):
        score.append((english_score(list[i][1]), list[i][1]))
    return max(score)[1]

