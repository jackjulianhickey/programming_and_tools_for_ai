"""Extension. Keep your keypresses, so you can experiment on them later.

Run the tests:

    python -m doctest W02/E08_save_history.py

No output means every test passed.

The lecture saved the *model* (the n-gram counts). This saves the *data* (what
you actually typed), which is more useful: from the data you can rebuild any
model you like, but from a model you cannot get the data back.

One line per session, so playing again adds to the file rather than replacing
it. E09_ngram_sweep.py reads what this writes.

Note each test below cleans up its own file at the end. Doctests run in
alphabetical order by function name, not the order they appear in the file, so
no test may depend on another having run first.
"""

from pathlib import Path

DATA = Path(__file__).parent / "data"


def history_path(student_id):
    """Return the file this student's sessions are saved in.

    >>> history_path("12345678").name
    'history_12345678.txt'

    It sits next to this source file, not next to wherever you ran python:

    >>> history_path("12345678").parent.name
    'data'
    """
    return DATA / f"history_{student_id}.txt"


def save_history(history, student_id):
    """Append one session to this student's file, as a single line.

    Use mode "a", not "w": a second session must not delete the first.

    >>> save_history("fdfd", "testA")
    >>> save_history("ddff", "testA")
    >>> print(open(history_path("testA")).read(), end="")
    fdfd
    ddff
    >>> history_path("testA").unlink()
    """
    p = history_path(student_id)
    with open(p, "a") as f:
        f.write(f"{history}\n")


def load_histories(student_id):
    """Return this student's sessions, oldest first, as a list of strings.

    Each line of the file is one session. Strip the newline off the end.

    >>> save_history("fdfd", "testB")
    >>> save_history("ddff", "testB")
    >>> load_histories("testB")
    ['fdfd', 'ddff']
    >>> history_path("testB").unlink()

    A student who has never played has no file, and so no sessions. That is
    not an error:

    >>> load_histories("nobody_at_all")
    []
    """
    p = history_path(student_id)
    hist = []
    if Path.exists(p):
        with open(p, "r") as f:
            for line in f:
                hist.append((line.rstrip('\n')))

    return  hist


def total_keys(student_id):
    """How many keypresses this student has contributed, over all sessions.

    >>> save_history("fdfd", "testC")
    >>> save_history("ddffdd", "testC")
    >>> total_keys("testC")
    10
    >>> history_path("testC").unlink()

    >>> total_keys("nobody_at_all")
    0
    """
    return sum(len(sessions) for sessions in load_histories(student_id))
