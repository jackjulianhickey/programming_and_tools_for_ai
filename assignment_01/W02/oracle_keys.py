"""Read one keypress, without waiting for Return. Given code: just use it.

    from oracle_keys import read_key
    key = read_key()

Windows and Unix do this in completely different ways, and neither is
pretty. That is why it is hidden in here.
"""

import sys


def read_key():
    """Return one keypress as a string, without waiting for Return."""
    if not sys.stdin.isatty():
        # Input is a file or a pipe, not a keyboard: fall back to a line.
        return sys.stdin.readline()[:1] or "\x04"

    try:
        import msvcrt                      # Windows only
    except ImportError:
        pass
    else:
        key = msvcrt.getwch()
        if key == "\x03":                  # Windows hands us Ctrl-C as a
            raise KeyboardInterrupt        # character, so we do the raising
        return key

    import termios, tty                    # Unix: macOS and Linux
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    try:
        # cbreak, not raw: cbreak leaves ISIG alone, so Ctrl-C still works.
        # TCSANOW, not the default TCSAFLUSH: TCSAFLUSH discards anything
        # typed before the mode switch, which loses the keypresses of a fast
        # typist -- and this game asks them to type fast.
        tty.setcbreak(fd, termios.TCSANOW)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)
