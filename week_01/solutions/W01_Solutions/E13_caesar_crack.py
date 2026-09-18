"""Extension. Letting the computer pick the right decoding. SOLUTION.

Run the tests:

    python -m doctest W01_Solutions/E13_caesar_crack.py

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
    for c in text.lower():
        if c in "etaoin":
            count += 1
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
    'ebiil tloia'
    """
    best_text = s
    best_score = -1
    for k, text in all_shifts(s):
        score = english_score(text)
        if score > best_score:
            best_score = score
            best_text = text
    return best_text


# ANSWER: the score is only a count of common letters, and on eleven
# characters that count is noise. 'ebiil tloia' happens to contain more
# e/t/a/o/i/n than 'hello world' does. The scoring rule is not wrong, it
# just has almost no evidence to work with. More text would fix it, and so
# would a better model: real letter frequencies rather than a flat count,
# or looking for common words like 'the'. We will meet this trade-off
# again in Week 4.
