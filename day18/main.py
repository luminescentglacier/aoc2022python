# --- Day 18: Boiling Boulders ---
from collections import defaultdict
from itertools import pairwise
from pathlib import Path
from typing import NamedTuple, Self

INPUT_FILE = Path(__file__).parent / "input.txt"


class Pos(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: Self) -> Self:
        return Pos(self.x + other.x, self.y + other.y, self.z + other.z)


def parse(s: str) -> list[Pos]:
    data = []
    for line in s.splitlines():
        data.append(Pos(*map(int, line.split(","))))
    return data


def part_1(s: str) -> int:
    coords = parse(s)
    axs = [
        (("x", "y"), "z"),
        (("x", "z"), "y"),
        (("y", "z"), "x"),
    ]
    sides = 0
    for (a0, a1), at in axs:
        view = defaultdict(list)
        for pos in coords:
            view[(getattr(pos, a0), getattr(pos, a1))].append(getattr(pos, at))

        for values in view.values():
            sides += 2  # edges
            for a, b in pairwise(sorted(values)):
                if abs(a - b) > 1:
                    sides += 2  # interior cavity
    return sides


def part_2(s: str) -> int:
    coords = set(parse(s))
    # box with the margin of 1
    x_min, x_max = min(pos.x for pos in coords) - 1, max(pos.x for pos in coords) + 1
    y_min, y_max = min(pos.y for pos in coords) - 1, max(pos.y for pos in coords) + 1
    z_min, z_max = min(pos.z for pos in coords) - 1, max(pos.z for pos in coords) + 1
    directions = (
        Pos(0, -1, 0),  # up
        Pos(0, 1, 0),  # down
        Pos(-1, 0, 0),  # left
        Pos(1, 0, 0),  # right
        Pos(0, 0, -1),  # backward
        Pos(0, 0, 1),  # forward
    )

    ext_sides = 0
    filled = set()
    queue = {Pos(0, 0, 0)}
    while queue:
        cur = queue.pop()
        filled.add(cur)
        for d in directions:
            node = cur + d
            if (
                x_min <= node.x <= x_max
                and y_min <= node.y <= y_max
                and z_min <= node.z <= z_max
                and node not in filled
            ):
                if node in coords:
                    ext_sides += 1
                else:
                    queue.add(node)
    return ext_sides


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
