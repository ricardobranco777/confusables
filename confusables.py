"""
Show homoglyphs and confusable characters
"""

import sys
from collections import defaultdict
from unicodedata import normalize


def parse(path: str) -> dict[str, set]:
    """
    Creates mapping from confusables.txt
    """
    mapping: dict[str, set] = accents()
    with open(path, encoding="utf-8") as file:
        lines = [
            line
            for line in file.read().splitlines()
            if line and not line.startswith("#")
        ]
    for line in lines:
        source, target, _ = line.split(";", 2)
        source = chr(int(source.strip(), 16))
        target = "".join(chr(int(s, 16)) for s in target.strip().split())
        mapping[target] |= {source, target}
    for target in list(mapping.keys()):
        for value in mapping[target]:
            mapping[value] = mapping[target]
    return mapping


def accents() -> dict[str, set]:
    """
    Creates mapping for accentable characters
    """
    mapping: dict[str, set] = defaultdict(set)
    for number in range(sys.maxunicode + 1):
        char = (
            normalize("NFD", chr(number))
            .encode("ascii", errors="ignore")
            .decode("utf-8")
        )
        if not char:
            continue
        mapping[char] |= {char, chr(number)}
    for target in list(mapping.keys()):
        for value in mapping[target]:
            mapping[value] = mapping[target]
    return mapping


if __name__ == "__main__":
    d = parse("confusables.txt")
    if len(sys.argv) == 1:
        sys.exit(f"Usage: {sys.argv[0]} CHAR...")
    for arg in sys.argv[1:]:
        print(" ".join(sorted(list(d[arg]))))
