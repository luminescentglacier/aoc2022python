# --- Day 4: Camp Cleanup ---

from pathlib import Path
from typing import Iterator

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    for line in s.splitlines():
        first, second = line.split(",", maxsplit=1)
        (a, b), (c, d) = first.split("-", maxsplit=1), second.split("-", maxsplit=1)
        yield (int(a), int(b)), (int(c), int(d))


def part_1(s: str) -> int:
    total = 0
    for (a_start, a_end), (b_start, b_end) in parse(s):
        a_size = a_end - a_start + 1
        b_size = b_end - b_start + 1

        if a_size > b_size:
            if b_start >= a_start and b_end <= a_end:
                total += 1
        else:
            if a_start >= b_start and a_end <= b_end:
                total += 1
    return total


def part_2(s: str) -> int:
    total = 0
    for (a_start, a_end), (b_start, b_end) in parse(s):
        a_size = a_end - a_start + 1
        b_size = b_end - b_start + 1

        if a_size > b_size:
            if a_start <= b_start <= a_end or a_start <= b_end <= a_end:
                total += 1
        else:
            if b_start <= a_start <= b_end or b_start <= a_end <= b_end:
                total += 1
    return total


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
