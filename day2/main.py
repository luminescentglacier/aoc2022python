from itertools import starmap
from pathlib import Path
from typing import Iterable

INPUT_FILE = Path(__file__).parent / "input.txt"

# Rock     A X
# Paper    B Y
# Scissors C Z


_choice_score = {"A": 1, "B": 2, "C": 3}

WIN = 6
DRAW = 3
LOOSE = 0


def choice_score(yours: str) -> int:
    return _choice_score[yours]


win_table = {"A": "B", "B": "C", "C": "A"}
loose_table = {v: k for k, v in win_table.items()}


def win_score(op: str, yours: str) -> int:
    if op == yours:
        return DRAW
    return WIN if yours == win_table[op] else LOOSE


def score(op: str, yours: str) -> int:
    return choice_score(yours) + win_score(op, yours)


def read_pairs(s: str) -> Iterable[tuple[str, str]]:
    tr_map = str.maketrans({"X": "A", "Y": "B", "Z": "C"})
    for line in s.splitlines():
        yield line.translate(tr_map).split(maxsplit=1)


def part_1(s: str) -> int:
    return sum(starmap(score, read_pairs(s)))


def part_2(s: str) -> int:
    total = 0
    for op, outcome in read_pairs(s):
        match outcome:
            case "A":  # loose
                total += score(op, loose_table[op])
            case "B":  # draw
                total += score(op, op)
            case "C":  # win
                total += score(op, win_table[op])
    return total


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
