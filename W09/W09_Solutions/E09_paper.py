"""Extension. Produce your own version of the paper. SOLUTION.

    python W09_Solutions/E09_paper.py     # prints the checklist below

There is no code to write here and no doctest to pass. What you hand in is a
pdf, and it has to be *yours*: run with a different random seed and every
number in it changes, so a paper with our numbers in it is a paper you did
not run.

THE STEPS

 1. Open E01_penguins.py and find the line

        SEED = 0

    Change the 0 to your student ID number, and save.

 2. Run it again.

        python E01_penguins.py

    It will notice. The program saves its raw results in results.csv along
    with the seed they came from, so a file written under the old seed is
    refused and the experiment runs again. It prints a line saying so. (The
    --fresh flag forces a re-run even when the seed has not changed; you
    should not need it.)

 3. Look at what it printed. The accuracies will have moved, and the best
    combination at the bottom may well be a different one. That is not a
    mistake: 266 penguins is not many, and which of them land in the test
    set genuinely matters.

 4. Go to the Overleaf project linked at the top of E01_penguins.py. Fork it
    to your own account -- you cannot edit mine -- and change the author line
    to your own name and ID.

 5. Upload the three files your run has just written, over the ones already
    there:

        table1.tex    table2.tex    accuracy.pdf

 6. Read the paper through. The prose quotes numbers -- the dummy
    classifier's score, how much normalisation is worth, where the peak in k
    is. Some of them will now be wrong. Fix them. This is the actual work of
    the exercise, and it is why a pdf is what we ask for: you cannot produce
    a correct one without having read your own results.

 7. Export the pdf from Overleaf, save it beside this file as paper.pdf, and
    submit it with the rest of your portfolio.

QUESTION: did the best combination change from the one in the lecture? Name
one number in the paper that you had to correct, and say why a different
seed moved it. Answer in the comment at the bottom of this file.
"""


CHECKLIST = [
    "SEED changed to your student ID in E01_penguins.py",
    "ran: python E01_penguins.py, and watched it re-run",
    "forked the Overleaf project to your own account",
    "author line changed to your name and ID",
    "uploaded table1.tex, table2.tex, accuracy.pdf",
    "corrected every number quoted in the prose",
    "exported the pdf and saved it as paper.pdf",
]


def main():
    print(__doc__.split("THE STEPS")[0].strip())
    print("\nChecklist:\n")
    for i, step in enumerate(CHECKLIST, 1):
        print(f"  {i}. [ ] {step}")


if __name__ == "__main__":
    main()


# ANSWER:
