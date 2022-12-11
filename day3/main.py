# --- Day 3: Rucksack Reorganization ---

from pathlib import Path
from typing import Iterable

INPUT_FILE = Path(__file__).parent / "input.txt"


def chunks(iterable: Iterable[str], size: int) -> Iterable[tuple[str, ...]]:
    args = [iter(iterable)] * size
    return zip(*args, strict=True)


def letter_score(letter: str) -> int:
    return ord(letter) - (96 if letter.islower() else 38)


def part_1(s: str) -> int:
    total = 0
    for sack in s.splitlines():
        middle = int(len(sack) / 2)
        common = set(sack[:middle]).intersection(sack[middle:]).pop()
        total += letter_score(common)
    return total


def part_2(s: str) -> int:
    total = 0
    for sacks in chunks(s.splitlines(), size=3):
        contents = (set(sack) for sack in sacks)
        common = set.intersection(*contents).pop()
        total += letter_score(common)
    return total


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
