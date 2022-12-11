# --- Day 6: Tuning Trouble ---

import timeit
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def find_marker(s: str, size: int) -> int:
    candidates = ((i + size, s[i : i + size]) for i in range(len(s) - size))
    for pos, packet in candidates:
        if len(set(packet)) == size:
            return pos


def find_marker_optimized(s: str, size: int) -> int:
    chars = set()
    beg = 0
    while beg < len(s):
        end = beg + size
        chars.update(s[beg:end])
        if len(chars) == size:
            return end

        missing = size - len(chars)
        for c in set(s[beg : beg + missing]):
            if c not in s[beg + missing : end]:
                chars.discard(c)
        beg = beg + missing


def part_1(s: str) -> int:
    return find_marker(s, 4)


def part_1_optimized(s: str) -> int:
    return find_marker_optimized(s, 4)


def part_2(s: str) -> int:
    return find_marker(s, 14)


def part_2_optimized(s: str) -> int:
    return find_marker_optimized(s, 14)


def bench(s: str):
    print("Bench")
    p1 = timeit.timeit(lambda: part_1(s), number=10000)
    p1_opt = timeit.timeit(lambda: part_1_optimized(s), number=10000)
    print(f"  Part 1: {p1 / p1_opt:.2f}x")
    p2 = timeit.timeit(lambda: part_2(s), number=10000)
    p2_opt = timeit.timeit(lambda: part_2_optimized(s), number=10000)
    print(f"  Part 2: {p2 / p2_opt:.2f}x")


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1_optimized(s)}")
    print(f"Part 2: {part_2_optimized(s)}")
    bench(s)
