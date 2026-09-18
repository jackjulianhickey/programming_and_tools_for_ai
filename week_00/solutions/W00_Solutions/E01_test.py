"""Drill. Check your setup. Nothing to write here, and nothing to hand in.

You need three ways of running Python this semester. 

1. As a script. In a terminal, in the folder that contains W00:

       python W00/E01_test.py

   Two lines should print, and no error. Later, we will use `python -m doctest` also.

2. In IPython, an interactive prompt. Run `ipython`, then type:

       import sys
       sys.executable

3. In a notebook. Run `jupyter lab`, `jupyter notebook`, or Google Colab; 
   make a new notebook, put those same two
   lines in a cell, and press Shift-Return to execute that cell.

If any of the three does not work, sort it out now, or bring it to the lab.

All three should report the same path. If they do not, you may have more than one
Python installed. It is not a big issue for now but can cause confusion later.
"""

import sys

if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    print("running from", sys.executable)
