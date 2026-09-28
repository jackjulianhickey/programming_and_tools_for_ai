"""Drill. Nothing to write here: the only job is to run this file. SOLUTION.

This is the bill of materials from the lecture, complete. Run its tests:

    python -m doctest W03_Solutions/E01_bom.py

No output means every test passed.

Then run it as a program, which prints the answers the scrap merchant wanted:

    python W03_Solutions/E01_bom.py

Read `unit_mass` until you are happy that the two cases are right: a part we
buy returns its own mass, and a part we build sums its children. That is the
whole of recursion, and everything else this week is a variation on it.
"""

import json
from pathlib import Path

DATA = Path(__file__).parent / "data"


def load_bom(filename):
    """Read a bill of materials from a JSON file in this file's data folder.

    >>> bicycle = load_bom("bicycle.json")
    >>> bicycle["name"]
    'bicycle'
    >>> len(bicycle["children"])
    5
    """
    with open(DATA / filename) as f:
        return json.load(f)


def everything(node):
    """Keep every part. The default question, which excludes nothing.

    >>> everything({"name": "spoke", "material": "steel"})
    True
    """
    return True


def is_steel(node):
    """Is this part made of steel?

    >>> is_steel({"name": "spoke", "material": "steel"})
    True
    >>> is_steel({"name": "tyre", "material": "rubber"})
    False
    """
    return node["material"] == "steel"


def unit_mass(node, keep=everything):
    """Total mass of one `node`, counting only the parts `keep` says yes to.

    A part we buy is the base case: it knows its own mass. A part we build is
    the recursive case: it is the sum of its children, each multiplied by how
    many of them go in.

    >>> bicycle = load_bom("bicycle.json")
    >>> unit_mass(bicycle)
    5180
    >>> unit_mass(bicycle, keep=is_steel)
    3220

    It works on any subtree, because a subtree is just a smaller bill:

    >>> wheel = bicycle["children"][0]
    >>> unit_mass(wheel)
    1060
    """
    if "mass" in node:
        return node["mass"] if keep(node) else 0
    return sum(c["qty"] * unit_mass(c, keep) for c in node["children"])


def parts(node):
    """Yield every part we buy, one at a time, left to right.

    >>> bicycle = load_bom("bicycle.json")
    >>> [p["name"] for p in parts(bicycle)]
    ['rim', 'spoke', 'hub', 'tyre', 'frame', 'handlebar', 'saddle', 'chain']

    It is a generator, so it has no length until you ask for the items:

    >>> len(list(parts(bicycle)))
    8
    """
    if "children" not in node:
        yield node
    else:
        for c in node["children"]:
            yield from parts(c)


if __name__ == "__main__":
    from collections import Counter

    bicycle = load_bom("bicycle.json")
    print(f"whole bicycle: {unit_mass(bicycle)} g")
    print(f"steel only:    {unit_mass(bicycle, keep=is_steel)} g")
    print("by material:  ", Counter(p["material"] for p in parts(bicycle)))
