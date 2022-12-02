from typing import Iterable
import bisect
import sys

try:
    FILE = sys.argv[1]
except IndexError:
    FILE = "test.txt"


def get_elfs() -> Iterable[int]:
    elf = 0
    with open(FILE) as file:
        for line in file.read().splitlines():
            if line:
                elf += int(line)
            else:
                yield elf
                elf = 0


def part_1() -> int:
    return max(get_elfs())


def part_2() -> int:
    top = 3
    leaders = []
    for elf in get_elfs():
        bisect.insort_right(leaders, elf)
        leaders = leaders[-top:]
    return sum(leaders)


if __name__ == "__main__":
    print(f"Input: {FILE}")
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")
