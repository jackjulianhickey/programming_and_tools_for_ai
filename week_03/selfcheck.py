"""Check your work, and build the zip you submit.

    python selfcheck.py W01            # a whole week
    python selfcheck.py W01/E01_first_last.py   # one problem
    python selfcheck.py --zip          # check everything, then build the zip

It reports three things:

  1. Does each file import cleanly, without hanging?
  2. Is every function we asked for present?
  3. Which functions pass their doctests?

An incomplete portfolio is fine: you get credit for what works. This script
just tells you what will and will not count, so there are no surprises.

--zip is how you submit. It finds your week folders, checks every file, and
writes submission_<your id>.zip containing your .py files and nothing else.
Hand that zip in. Never build one by hand: the layout has to be exactly
right, and this gets it right. If --zip is not recognised, you are running
an old copy of selfcheck.py -- take the one from the latest week's zip.
"""

import datetime
import doctest
import importlib.util
import json
import subprocess
import sys
import traceback
import zipfile
from pathlib import Path

TIMEOUT = 60

# Printed at the top of a --zip run and recorded inside the zip, so that a
# submission can be traced back to the script that built it.
VERSION = "2026-09-23"

MANIFEST = {
    "W00": {
        # Given code: run it, check your setup, change nothing.
        "E01_test.py": [],
    },
    "W01": {
        # An empty list means nothing in the file is the student's work: it is
        # given code, and make_stubs.py copies it through untouched.
        "E01_newton.py": [],
        "E02_first_last.py": ["first_last"],
        "E03_slices.py": ["middle", "last_three"],
        "E04_count_vowels.py": ["count_vowels"],
        "E05_squares.py": ["squares"],
        "E06_cumsum.py": ["cumsum"],
        "E07_product.py": ["product"],
        "E08_palindrome.py": ["is_palindrome"],
        "E09_hailstones.py": ["hailstones", "longest_hailstone"],
        "E10_hailstones_iterate.py": ["hailstone_step", "reaches_one"],
        "E11_rotate.py": ["rotate"],
        "E12_caesar_shifts.py": ["all_shifts"],
        "E13_caesar_crack.py": ["english_score", "crack"],
        "E14_newton_cbrt.py": ["newton_cbrt"],
        "E15_gcd.py": ["gcd"],
    },
    "W02": {
        # Given code, not exercises: the empty list means make_stubs.py copies
        # them through untouched, so students get the working game.
        "E01_oracle.py": [],
        "oracle_keys.py": [],
        "E02_get_or.py": ["get_or"],
        "E03_invert_dict.py": ["invert_dict"],
        "E04_merge.py": ["merge"],
        "E05_tally.py": ["tally", "tally_counter"],
        "E06_group_by.py": ["group_by_first_letter"],
        "E07_key_stats.py": ["longest_run", "switch_rate"],
        "E08_save_history.py": ["history_path", "save_history",
                                "load_histories", "total_keys"],
        "E09_ngram_sweep.py": ["accuracy", "sweep"],
    },
    "W03": {
        # Given code: run it, read it, change nothing. See W01/E01_newton.py.
        "E01_bom.py": [],
        "E02_sort_by_key.py": ["sort_by_mass", "heaviest"],
        "E03_nested_sum.py": ["nested_sum"],
        "E04_flatten.py": ["flatten"],
        "E05_count_parts.py": ["count_parts", "deepest"],
        "E06_apply_fn.py": ["apply_fn_to_list", "apply_fn_to_list_gen"],
        "E07_part_paths.py": ["part_paths", "find_part"],
        "E08_bom_json.py": ["load_bom", "repriced", "save_bom"],
    },
    "W04": {
        # Given code: run it, read it, change nothing. See W01/E01_newton.py.
        "E01_SimpleDict.py": [],
        "E02_bucket_index.py": ["bucket_index"],
        "E03_is_hashable.py": ["is_hashable"],
        "E04_string_collision.py": ["find_collision"],
        # E05 and E06 each carry their own copy of SimpleDict as given code,
        # rather than importing E01's and subclassing it: inheritance is not
        # taught this week. E06's copy includes E05's __delitem__.
        "E05_delitem.py": ["SimpleDict.__delitem__"],
        "E06_fast_contains.py": ["SimpleDict.__contains__"],
    },
    "W06": {
        # Given code: run it, read it, change nothing. See W01/E01_newton.py.
        # It holds both of the week's graphs: the river and the road map.
        "E01_river.py": [],
        "E02_neighbours.py": ["neighbours", "is_edge", "degree"],
        "E03_reachable.py": ["reachable", "connected"],
        "E04_hops.py": ["hops_from", "farthest_hops"],
        "E05_calculator.py": ["calc_successors", "presses", "fewest_presses"],
        "E06_route.py": ["time_lost", "quickest_times"],
    },
    "W07": {
        # Given code: run it, read it, change nothing. See W01/E01_newton.py.
        # It holds the whole lecture program: Fibonacci slow and cached, the
        # edit-distance table, the traceback, and DTW.
        "E01_editdist.py": [],
        "E02_hamming.py": ["hamming", "hamming_padded"],
        "E03_fib_table.py": ["fib_table", "fib_pair"],
        "E04_one_row.py": ["levenshtein_row"],
        "E05_spell.py": ["suggest"],
        "E06_wrong_tool.py": ["levenshtein_tol", "dtw_symbols"],
    },
    "W08": {
        # Given code: run it, read it, change nothing. See W01/E01_newton.py.
        # prep_data.py fetches the photos; it is not an exercise either.
        "E01_photos.py": [],
        "prep_data.py": [],
        "E02_vectorise.py": ["softplus"],
        "E03_broadcast.py": ["combine", "times_table"],
        "E04_axis_masks.py": ["count_above", "values_above",
                              "column_means", "row_maxes"],
        "E05_broadcastable.py": ["is_broadcastable"],
        "E06_heatmap.py": ["distance_matrix"],
        "E07_brightness.py": ["brightness", "darkest_first"],
        "E08_grayscale.py": ["to_gray"],
    },
    "W09": {
        # Given code: run it, read it, change nothing. See W01/E01_newton.py.
        # It holds the whole experiment: the cleaning, our own k-NN, the
        # factorial grid, the two tables and the figure. data/penguins.csv
        # is the published data, shipped as-is.
        "E01_penguins.py": [],
        "E02_select.py": ["column_list", "heavier_than"],
        "E03_summary.py": ["column_range", "column_mean", "spread"],
        "E04_groups.py": ["group_sizes", "group_means"],
        "E05_missing.py": ["count_missing", "drop_missing", "fill_with_median"],
        "E06_pivot.py": ["wide", "best_by"],
        "E07_dummies.py": ["encode", "n_new_columns"],
        "E08_estimator.py": ["train", "label_for", "accuracy"],
        # No code to write: the deliverable is a pdf. Given code, so
        # make_stubs.py copies it through. See W01/E01_newton.py.
        "E09_paper.py": [],
    },
}


def week_of(path):
    """Which week does this file belong to? Look at its folder name."""
    name = path.parent.name.split("_Solutions")[0]
    return name if name in MANIFEST else None


def student_traceback(e):
    """Format the error, hiding the frames inside selfcheck and importlib."""
    tb = e.__traceback__
    hide = (Path(__file__).name, "<frozen importlib._bootstrap>",
            "<frozen importlib._bootstrap_external>")
    while tb is not None and Path(tb.tb_frame.f_code.co_filename).name in hide:
        tb = tb.tb_next
    return "".join(traceback.format_exception(type(e), e, tb))


def resolve(mod, name):
    """Look up "func" or "Class.method" in an imported module."""
    obj = mod
    for part in name.split("."):
        obj = getattr(obj, part, None)
        if obj is None:
            return None
    return obj


def check(path):
    """Import one file and test it. Runs in a child process."""
    path = Path(path)
    week = week_of(path)
    required = MANIFEST.get(week, {}).get(path.name)

    # The file's own folder goes on sys.path first, so that a week's files can
    # import each other the same way they do when run directly -- W02's oracle
    # does `from oracle_keys import read_key`. spec_from_file_location does not
    # do this for us.
    sys.path.insert(0, str(path.parent.resolve()))

    spec = importlib.util.spec_from_file_location("submission", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not required:
        required = [n for n in vars(mod)
                    if callable(getattr(mod, n)) and not n.startswith("_")
                    and getattr(getattr(mod, n), "__module__", "") == "submission"]

    finder = doctest.DocTestFinder()
    results = []

    # The module docstring can hold doctests of its own: a hint at the top of
    # the file, or, where the student's job is to write a whole class, the
    # specification itself -- there is no class docstring to put it in until
    # they write the class. DocTestFinder reached from a function or class name
    # never sees these, so parse the module docstring directly.
    doc = doctest.DocTestParser().get_doctest(
        mod.__doc__ or "", dict(vars(mod)), "module docstring", str(path), 0)
    if doc.examples:
        runner = doctest.DocTestRunner(verbose=False)
        runner.run(doc, out=lambda s: None)
        results.append(("module docstring",
                        "pass" if runner.failures == 0 else "fail",
                        runner.tries, runner.failures))

    for name in required:
        obj = resolve(mod, name)
        if obj is None:
            results.append((name, "missing", 0, 0))
            continue
        attempted = failed = 0
        for t in finder.find(obj, name, globs=dict(vars(mod))):
            if not t.examples:
                continue
            runner = doctest.DocTestRunner(verbose=False)
            runner.run(t, out=lambda s: None)
            attempted += runner.tries
            failed += runner.failures
        if attempted == 0:
            results.append((name, "no doctests", 0, 0))
        else:
            results.append((name, "pass" if failed == 0 else "fail", attempted, failed))
    return results


def check_one(path):
    """Run check() in a child process. Return (results, error_message)."""
    try:
        proc = subprocess.run(
            [sys.executable, __file__, "--child", str(path)],
            capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, (
            f"TIMED OUT after {TIMEOUT}s while importing this file.\n"
            "Something in it never finished. Check for an infinite loop, or\n"
            "for code (or input()) at the bottom of the file that is not\n"
            'inside:  if __name__ == "__main__":')
    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None, (proc.stderr or proc.stdout or "no output").strip()
    if isinstance(data, dict):
        return None, data["error"].rstrip()
    return data, None


def report(paths):
    """Check each file, printing as it goes. Return the printed lines.

    --zip keeps the lines and puts them in the zip, so returning them saves
    running everything twice.
    """
    lines = []

    def emit(line=""):
        print(line)
        lines.append(line)

    passed = total = failures = 0
    first_bad = None
    for path in paths:
        emit(f"\n{path}")
        if not path.exists():
            emit("  MISSING FILE")
            continue
        results, error = check_one(path)
        if error:
            emit("  DID NOT RUN. Python said:\n")
            emit("    " + error.replace("\n", "\n    ") + "\n")
            first_bad = first_bad or path
            continue
        for name, status, attempted, failed in results:
            total += 1
            if status == "pass":
                emit(f"  PASS     {name}  ({attempted} doctests)")
                passed += 1
            elif status == "fail":
                emit(f"  FAIL     {name}  ({failed} of {attempted} doctests failed)")
                failures += 1
                first_bad = first_bad or path
            elif status == "missing":
                emit(f"  MISSING  {name}  (not defined in this file)")
                failures += 1
                first_bad = first_bad or path
            else:
                emit(f"  ?        {name}  ({status})")

    # W00 has one file with nothing in it to test, so "0 of 0" is the right
    # answer there and is not a complaint. Only offer the hint if something
    # actually went wrong.
    if total == 0:
        emit("\nNothing here has doctests. Nothing to check.\n")
    else:
        emit(f"\n{passed} of {total} checks pass.")
        if failures:
            emit("To see why one failed, run its doctests directly, eg:")
            emit(f"    python -m doctest {first_bad or paths[0]}\n")
        else:
            emit("")
    return lines


def find_weeks(root=None):
    """Find the W01, W02, ... folders, wherever they were unzipped.

    Unzipping by double-click often wraps a week in a folder of its own name,
    so W01/E02_first_last.py may really be at W01/W01/E02_first_last.py. Look
    in this folder and one level below it, and accept a candidate only if it
    holds at least one of the files we expect -- otherwise the wrapper folder
    would be mistaken for the week itself.
    """
    root = Path(root or ".")
    bases = [root] + sorted(d for d in root.iterdir() if d.is_dir())
    found = {}
    for week, files in sorted(MANIFEST.items()):
        for base in bases:
            cand = base / week
            if cand.is_dir() and any((cand / f).exists() for f in files):
                found[week] = cand
                break
    return found


def zip_submission(student_id=None):
    """Check every week we can find, then write the zip to submit."""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"selfcheck.py {VERSION}   {stamp}")

    weeks = find_weeks()
    if not weeks:
        print(f"\nI cannot find any week folders (W01, W02, ...) here:\n"
              f"    {Path.cwd()}\n"
              f"Run this from the folder that holds them.")
        return 2

    print("Found: " + ", ".join(f"{w} ({weeks[w]})" for w in sorted(weeks)))

    if student_id is None:
        student_id = input("Your student ID number: ")
    # The ID becomes a filename, so keep it to characters that are safe in one.
    student_id = "".join(c for c in student_id if c.isalnum()) or "unknown"

    paths = [weeks[w] / f for w in sorted(weeks) for f in MANIFEST[w]]
    lines = report(paths)

    # The zip is built from MANIFEST, not from whatever is lying around, so it
    # contains your .py files under W01/, W02/, ... and nothing else: no
    # solutions, no data folders, no __pycache__, no editor leftovers.
    zip_path = Path(f"submission_{student_id}.zip")
    written = missing = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for week in sorted(weeks):
            for name in MANIFEST[week]:
                path = weeks[week] / name
                if path.exists():
                    z.write(path, f"{week}/{name}")
                    written += 1
                else:
                    missing += 1
        header = [f"selfcheck.py {VERSION}", f"built {stamp}",
                  f"student id {student_id}", f"python {sys.version.split()[0]}",
                  f"folder {Path.cwd()}", ""]
        z.writestr("submission_report.txt", "\n".join(header + lines) + "\n")

    print(f"\nAll done. I wrote {zip_path}, holding {written} of your files.")
    if missing:
        print(f"{missing} of the files I looked for were not there, which is "
              f"fine\nif you have not got to them yet.")
    print("That is the file to hand up, just as it is -- no need to rename\n"
          "it or repackage it.")
    print("\nOne thing worth saying about the numbers above: they come from "
          "the\ndoctests in your own files, so take them as a guide rather "
          "than a grade.\nThe marks come from a separate set of tests and "
          "from the interview, and\nwork that runs still counts even when "
          "something else nearby does not.")
    print("\nGood luck.")
    return 0


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--child":
        try:
            print(json.dumps(check(sys.argv[2])))
        except Exception as e:
            print(json.dumps({"error": student_traceback(e)}))
        return 0

    # "--zip" or "--zip 12345678": the student ID may be given on the command
    # line, or typed when asked for.
    if len(sys.argv) in (2, 3) and sys.argv[1] == "--zip":
        return zip_submission(sys.argv[2] if len(sys.argv) == 3 else None)

    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    target = Path(sys.argv[1])
    if target.is_dir():
        week = target.name.split("_Solutions")[0]
        if week not in MANIFEST:
            print(f"I don't know week {week}. Expected one of: "
                  f"{', '.join(sorted(MANIFEST))}")
            return 2
        paths = [target / f for f in MANIFEST[week]]
    elif target.exists():
        paths = [target]
    else:
        print(f"No such file or folder: {target}")
        return 2

    report(paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
