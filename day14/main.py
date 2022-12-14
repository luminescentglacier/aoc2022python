# --- Day 14: Regolith Reservoir ---

from enum import Enum, auto
from pathlib import Path
from typing import NamedTuple, Self

from more_itertools import windowed

INPUT_FILE = Path(__file__).parent / "input.txt"


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def parse(cls, s: str) -> Self:
        x, y = map(int, s.split(","))
        return cls(x, y)


def parse(s: str) -> list[list[Point]]:
    paths = []
    for line in s.splitlines():
        points = [Point.parse(p) for p in line.split(" -> ")]
        paths.append(points)
    return paths


class Tile(Enum):
    Rock = auto()
    Air = auto()
    Sand = auto()

    @property
    def solid(self) -> bool:
        return self != Tile.Air

    def __str__(self) -> str:
        match self:
            case self.Rock:
                return "#"
            case self.Air:
                return "."
            case self.Sand:
                return "o"


def line_from_points(beg: Point, end: Point) -> list[Point]:
    line = []
    if beg.x == end.x:
        up, down = beg.y, end.y
        if up < down:
            up, down = down, up
        for y in range(down, up + 1):
            line.append(Point(beg.x, y))
    else:
        right, left = beg.x, end.x
        if right < left:
            right, left = left, right
        for x in range(left, right + 1):
            line.append(Point(x, beg.y))
    return line


class Game:
    nodes: dict[Point, Tile]  # if all you have is a hammer...
    height: int
    origin: Point = Point(500, 0)
    moving: Point | None = None
    total: int = 0
    game_over: bool = False

    def __init__(self, structures: list[list[Point]]) -> None:
        self.nodes = {}
        for struct in structures:
            for beg, end in windowed(struct, 2):
                self.nodes.update({p: Tile.Rock for p in line_from_points(beg, end)})
        self.height = sorted((n.y for n in self.nodes.keys()), reverse=True)[0] + 2

    @property
    def horizontal_bounds(self) -> tuple[int, int]:
        xs = sorted((n.x for n in self.nodes.keys()))
        return xs[0], xs[-1]

    def display(self):
        left, right = self.horizontal_bounds
        for y in range(0, self.height + 1):
            for x in range(left + 5, right + 5 + 1):
                if tile := self.nodes.get(Point(x, y)):
                    print(str(tile), end="")
                else:
                    print(str(Tile.Air), end="")
            print()

    def tick(self, stop_on_reaching_abyss: bool = False):
        if self.moving is None:
            self.total += 1
            self.nodes[self.origin] = Tile.Sand
            self.moving = self.origin
            return

        prev = self.moving
        down = Point(self.moving.x, self.moving.y + 1)
        down_left = Point(self.moving.x - 1, self.moving.y + 1)
        down_right = Point(self.moving.x + 1, self.moving.y + 1)

        if down.y == self.height:
            self.moving = None
            return

        if stop_on_reaching_abyss and down.y == self.height - 1:
            raise RuntimeError("Reached the abyss!")
        elif down not in self.nodes:
            if down.y == self.height:
                self.moving = None
            else:
                self.nodes[down] = Tile.Sand
                self.moving = down
                del self.nodes[prev]
        elif down_left not in self.nodes:
            self.nodes[down_left] = Tile.Sand
            self.moving = down_left
            del self.nodes[prev]
        elif down_right not in self.nodes:
            self.nodes[down_right] = Tile.Sand
            self.moving = down_right
            del self.nodes[prev]
        elif self.moving == self.origin:
            raise RuntimeError("No space left!")
        else:
            self.moving = None


def part_1(s: str) -> int:
    game = Game(list(parse(s)))
    while True:
        try:
            game.tick(stop_on_reaching_abyss=True)
        except RuntimeError:
            return game.total - 1


def part_2(s: str) -> int:
    game = Game(list(parse(s)))
    while True:
        try:
            game.tick()
        except RuntimeError:
            return game.total


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
