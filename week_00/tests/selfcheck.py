"""Check your work before you submit it.

    python selfcheck.py W01            # a whole week
    python selfcheck.py W01/E01_first_last.py   # one problem

It reports three things:

  1. Does each file import cleanly, without hanging?
  2. Is every function we asked for present?
  3. Which functions pass their doctests?

An incomplete portfolio is fine: you get credit for what works. This script
just tells you what will and will not count, so there are no surprises.
"""

import doctest
import importlib.util
import json
import subprocess
import sys
import traceback
from pathlib import Path

TIMEOUT = 60

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
        "E05_delitem.py": ["DeletableDict.__delitem__"],
        "E06_mutable_keys.py": ["to_hashable", "store_and_mutate"],
        "E07_fast_contains.py": ["FastDict.__contains__"],
    },
    "W05": {
        # Review week: one given file, a revision sheet you run. Nothing here
        # is the student's work. See W00/E01_test.py.
        "E01_review.py": [],
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
    passed = total = failures = 0
    for path in paths:
        print(f"\n{path}")
        if not path.exists():
            print("  MISSING FILE")
            continue
        results, error = check_one(path)
        if error:
            print("  DID NOT RUN. Python said:\n")
            print("    " + error.replace("\n", "\n    ") + "\n")
            continue
        for name, status, attempted, failed in results:
            total += 1
            if status == "pass":
                print(f"  PASS     {name}  ({attempted} doctests)")
                passed += 1
            elif status == "fail":
                print(f"  FAIL     {name}  ({failed} of {attempted} doctests failed)")
                failures += 1
            elif status == "missing":
                print(f"  MISSING  {name}  (not defined in this file)")
                failures += 1
            else:
                print(f"  ?        {name}  ({status})")

    # W00 has one file with nothing in it to test, so "0 of 0" is the right
    # answer there and is not a complaint. Only offer the hint if something
    # actually went wrong.
    if total == 0:
        print("\nNothing here has doctests. Nothing to check.\n")
    else:
        print(f"\n{passed} of {total} functions pass.")
        if failures:
            print("To see why one failed, run its doctests directly, eg:")
            print(f"    python -m doctest {paths[0]}\n")
        else:
            print()


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--child":
        try:
            print(json.dumps(check(sys.argv[2])))
        except Exception as e:
            print(json.dumps({"error": student_traceback(e)}))
        return 0

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
