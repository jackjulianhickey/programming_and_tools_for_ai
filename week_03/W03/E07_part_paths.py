"""Extension. Carrying information down the recursion.

Run the tests:

    python -m doctest W03/E07_part_paths.py

No output means every test passed.
"""

# Given: the bicycle from the lecture. You do not need to change it.
bicycle = {
    "name": "bicycle", "qty": 1, "children": [
        {"name": "wheel", "qty": 2, "children": [
            {"name": "rim",   "qty": 1,  "material": "aluminium", "mass": 380},
            {"name": "spoke", "qty": 32, "material": "steel",     "mass": 5},
            {"name": "hub",   "qty": 1,  "material": "steel",     "mass": 200},
            {"name": "tyre",  "qty": 1,  "material": "rubber",    "mass": 320},
        ]},
        {"name": "frame",     "qty": 1, "material": "steel",     "mass": 2200},
        {"name": "handlebar", "qty": 1, "material": "aluminium", "mass": 300},
        {"name": "saddle",    "qty": 1, "material": "plastic",   "mass": 260},
        {"name": "chain",     "qty": 1, "material": "steel",     "mass": 300},
    ],
}


def part_paths(node, prefix=""):
    """Return the full path of every part you buy, deepest name last.

    Everything so far has passed answers back up the tree. This passes
    something down: each call builds the path of the node it is looking at
    and hands it to its children, exactly as depth was handed down in the
    lecture's debugging version of unit_mass.

    prefix is where the caller is; do not set it yourself when you call
    part_paths from outside.

    >>> for path in part_paths(bicycle):
    ...     print(path)
    bicycle/wheel/rim
    bicycle/wheel/spoke
    bicycle/wheel/hub
    bicycle/wheel/tyre
    bicycle/frame
    bicycle/handlebar
    bicycle/saddle
    bicycle/chain

    The path of a part depends on where you started, not on where it lives:

    >>> part_paths(bicycle["children"][0])
    ['wheel/rim', 'wheel/spoke', 'wheel/hub', 'wheel/tyre']
    >>> part_paths(bicycle["children"][1])
    ['frame']
    """
    part = (f"{prefix}/{node['name']}") if prefix else node["name"]
    if "children" not in node:
        return [part]

    paths = []
    for child in node["children"]:
        paths.extend(part_paths(child, part))
    return paths


def find_part(node, path):
    """Return the part at the given path, or raise KeyError if there is none.

    >>> find_part(bicycle, "bicycle/wheel/hub")["mass"]
    200
    >>> find_part(bicycle, "bicycle/frame")["material"]
    'steel'
    >>> find_part(bicycle, "bicycle")["name"]
    'bicycle'
    >>> find_part(bicycle, "bicycle/wheel/axle")
    Traceback (most recent call last):
        ...
    KeyError: 'bicycle/wheel/axle'
    """
    parts = path.split('/')
    if parts[0] != node["name"]:
        raise KeyError(f"{path}")

    if len(parts) == 1:
        return node

    for child in node.get("children", []):
        if child["name"] == parts[1]:
            remaining_path = "/".join(parts[1:])
            try:
                return find_part(child, remaining_path)
            except:
                raise KeyError(f"{path}")
    raise KeyError(f"{path}")


