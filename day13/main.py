# --- Day 13: Distress Signal ---

from functools import cmp_to_key
from itertools import zip_longest
from pathlib import Path

from more_itertools import flatten

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str):
    for pairs in s.split("\n\n"):
        first, second = pairs.splitlines()
        yield eval(first), eval(second)  # lol


def compare(first, second) -> int:
    for left, right in zip_longest(first, second):
        match left, right:
            case None, _:
                return -1
            case _, None:
                return +1

            case int(left), int(right):
                if left < right:
                    return -1
                elif left > right:
                    return +1

            case list(left), list(right):
                if (res := compare(left, right)) != 0:
                    return res
            case list(left), int(right):
                if (res := compare(left, [right])) != 0:
                    return res
            case int(left), list(right):
                if (res := compare([left], right)) != 0:
                    return res

    return 0


def part_1(s: str) -> int:
    correct = []
    for i, (left, right) in enumerate(parse(s), start=1):
        if compare(left, right) == -1:
            correct.append(i)
    return sum(correct)


def part_2(s: str) -> int:
    divs = [[2]], [[6]]
    packets = list(flatten(parse(s)))
    packets.extend(divs)

    order = sorted(packets, key=cmp_to_key(compare))
    return (order.index(divs[0]) + 1) * (order.index(divs[1]) + 1)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
