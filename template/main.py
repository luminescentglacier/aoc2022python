from pathlib import Path


def part_1(s: str) -> int:
    ...


def part_2(s: str) -> int:
    ...


if __name__ == "__main__":
    s = Path("input.txt").read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
