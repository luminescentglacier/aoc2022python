# --- Day 9: Rope Bridge ---

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Self

INPUT_FILE = Path(__file__).parent / "input.txt"


def motions(s: str) -> Iterable[tuple[str, int]]:
    for line in s.splitlines():
        direction, count = line.split()
        yield direction, int(count)


FLEX = 1


@dataclass
class Pos:
    x: int
    y: int

    def follow(self, towards: Self):
        vector = Pos((towards.x - self.x), (towards.y - self.y))
        x, y = abs(vector.x), abs(vector.y)
        if max(x, y) > FLEX:  # lmax distance
            self.x = self.x + int(math.copysign(min(x, FLEX), vector.x))
            self.y = self.y + int(math.copysign(min(y, FLEX), vector.y))


def part_1(s: str) -> int:
    visited = set()
    tail, head = Pos(0, 0), Pos(0, 0)
    for dir, cnt in motions(s):
        for _ in range(cnt):
            match dir:
                case "L":
                    head.x -= 1
                case "R":
                    head.x += 1
                case "U":
                    head.y += 1
                case "D":
                    head.y -= 1
            tail.follow(head)
            visited.add((tail.x, tail.y))
    return len(visited)


def part_2(s: str) -> int:
    visited = set()
    rope = [Pos(0, 0) for _ in range(10)]
    for dir, cnt in motions(s):
        for _ in range(cnt):
            match dir:
                case "L":
                    rope[0].x -= 1
                case "R":
                    rope[0].x += 1
                case "U":
                    rope[0].y += 1
                case "D":
                    rope[0].y -= 1
            for head, tail in zip(rope[:-1], rope[1:]):
                tail.follow(head)
            visited.add((rope[-1].x, rope[-1].y))
    return len(visited)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
