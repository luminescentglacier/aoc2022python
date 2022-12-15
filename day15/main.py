# --- Day 15: Beacon Exclusion Zone ---

import re
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).parent / "input.txt"

Y = 2_000_000
MAX = 4000000

PATTERN = re.compile(r"-?\d+")


class Pos(NamedTuple):
    x: int
    y: int


@dataclass
class Sensor:
    pos: Pos
    radius: int = field(init=False)

    beacon: InitVar[Pos]

    def __post_init__(self, beacon: Pos):
        self.radius = l1(self.pos, beacon)

    def range_at_y(self, y: int) -> tuple[int, int] | None:
        dy = abs(self.pos.y - y)
        width = max(self.radius - dy, 0)
        if width == 0:
            return None
        return self.pos.x - width, self.pos.x + width


def l1(a: Pos, b: Pos) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def parse(s: str) -> tuple[list[Sensor], set[Pos]]:
    beacons = set()
    sensors = []
    for line in s.splitlines():
        sx, sy, bx, by = map(int, PATTERN.findall(line))
        beacon = Pos(bx, by)
        sensor = Sensor(Pos(sx, sy), beacon)
        beacons.add(beacon)
        sensors.append(sensor)
    return sensors, beacons


def concat_ranges(ranges: list[tuple[int, int]]):
    ranges = sorted(ranges)
    concatenated = []
    left, right = ranges[0]
    for left_new, right_new in ranges[1:]:
        if left_new > (right + 1):
            concatenated.append((left, right))
            left, right = left_new, right_new
        else:
            right = max(right, right_new)
    else:
        concatenated.append((left, right))
    return concatenated


def part_1(raw: str) -> int:
    sensors, beacons = parse(raw)

    beacons_at_y = {b for b in beacons if b.y == Y}
    ranges = [r for s in sensors if (r := s.range_at_y(Y))]

    total = 0
    for l, r in concat_ranges(ranges):
        total += r - l + 1  # inclusive
        total -= sum(1 for b in beacons_at_y if l <= b.x <= r)
    return total


def part_2(raw: str) -> int:
    sensors, beacons = parse(raw)

    for y in range(MAX):
        ranges = [r for s in sensors if (r := s.range_at_y(y))]
        ranges.extend((b.x, b.x) for b in beacons if b.y == y)

        concatenated = concat_ranges(ranges)
        if len(concatenated) > 1:
            lost_beacon_x = concatenated[0][1] + 1  # assuming only one beacon is lost
            return lost_beacon_x * 4000000 + y
    raise ValueError("Guess they are lost forever...")


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
