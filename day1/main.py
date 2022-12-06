import bisect
from pathlib import Path
from typing import Iterable

INPUT_FILE = Path(__file__).parent / "input.txt"


def get_elfs(s: str) -> Iterable[int]:
    for elf in s.split("\n\n"):
        yield sum(map(int, elf.splitlines()))


def part_1(s: str) -> int:
    return max(get_elfs(s))


def part_2(s: str) -> int:
    top = 3
    leaders = []
    for elf in get_elfs(s):
        bisect.insort_right(leaders, elf)
        leaders = leaders[-top:]
    return sum(leaders)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
