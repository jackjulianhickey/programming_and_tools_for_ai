"""Extension. The bill of materials as a file you can change.

Run the tests:

    python -m doctest W03/E08_bom_json.py

No output means every test passed.
"""

import json
from pathlib import Path

DATA = Path(__file__).parent / "data"


# Given: unit_mass from the lecture, with the extra argument promised there.
# key says which number to add up, so the same function weighs or prices.
# You do not need to change it.
def everything(node):
    return True


def unit_total(node, key="mass", keep=everything):
    """Total node[key] over one of node, counting only parts keep() accepts."""
    if "children" not in node:
        return node[key] if keep(node) else 0
    return sum(c["qty"] * unit_total(c, key, keep) for c in node["children"])


def load_bom(filename):
    """Read a bill of materials from a JSON file in the data folder.

    >>> bom = load_bom("bicycle.json")
    >>> bom["name"]
    'bicycle'
    >>> round(unit_total(bom, key="cost"), 2)
    279.6
    """
    with open (DATA / filename) as f:
        bom = json.load(f)
    return bom


def repriced(node, material, factor):
    """Return a new tree with the cost of every `material` part multiplied.

    The tree that was passed in must not be changed: the supplier's price
    rise is a new version of the bill of materials, not an edit of the one
    already in memory. So build a new dict at every level rather than
    assigning into the old one.

    >>> bom = load_bom("bicycle.json")
    >>> dearer = repriced(bom, "steel", 1.10)
    >>> round(unit_total(dearer, key="cost"), 2)
    295.46

    Everything else is untouched -- the masses, and the parts made of
    anything but steel:

    >>> unit_total(dearer) == unit_total(bom)
    True
    >>> round(unit_total(bom, key="cost"), 2)
    279.6
    """
    new_node = dict(node) 
    if "children" in node:
        new_node["children"] = [repriced(child, material, factor) for child in node["children"]]
    if node.get("material") == material:
        new_node["cost"] = node["cost"] * factor
    return new_node


def save_bom(bom, path):
    """Write a bill of materials out as JSON.

    json.dump writes to an open file, so it needs a `with` block just as
    reading did. indent=4 makes the file readable by a human as well as by
    a program.

    A round trip through a file should change nothing at all:

    >>> import tempfile
    >>> bom = load_bom("bicycle.json")
    >>> dearer = repriced(bom, "steel", 1.10)
    >>> path = Path(tempfile.mkdtemp()) / "dearer.json"
    >>> save_bom(dearer, path)
    >>> with open(path) as f:
    ...     reloaded = json.load(f)
    >>> reloaded == dearer
    True
    >>> round(unit_total(reloaded, key="cost"), 2)
    295.46
    """

    with open((DATA / path), "w") as f:
        json.dump(bom, f, indent=4)
