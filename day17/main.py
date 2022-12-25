# --- Day 17: Pyroclastic Flow ---
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import Iterable, Self

from more_itertools import flatten, peekable

INPUT_FILE = Path(__file__).parent / "input.txt"

WIDTH = 7

ROCKS = (
    ("..@@@@.",),
    (
        "...@...",
        "..@@@..",
        "...@...",
    ),
    (
        "....@..",
        "....@..",
        "..@@@..",
    ),
    (
        "..@....",
        "..@....",
        "..@....",
        "..@....",
    ),
    (
        "..@@...",
        "..@@...",
    ),
)
EMPTY_ROW = "." * WIDTH


@dataclass
class Pos:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Pos(self.x + other.x, self.y + other.y)


class Game:
    chamber: list[list[str]]
    rock_queue: "peekable[tuple[int, tuple[str]]]"
    jet_queue: "peekable[tuple[int, str]]"

    falling: list[Pos]

    stopped_rocks: int = 0
    _height_base: int = 0

    def __init__(self, jets: str):
        self.chamber = []
        self.rock_queue = peekable(cycle(enumerate(ROCKS)))
        self.jet_queue = peekable(cycle(enumerate(jets)))
        self.falling = []

    @property
    def height(self):
        return self._height_base + self._height_current

    @property
    def _height_current(self) -> int:
        for i, row in enumerate(reversed(self.chamber)):
            if "#" in row:
                return len(self.chamber) - i
        return 0

    def round(self):
        while True:
            self._tick()
            if not self.falling:
                break

    def _tick(self):
        if not self.falling:
            self._spawn()

        _, jet = next(self.jet_queue)
        match jet:
            case ">":
                jet_delta = Pos(1, 0)
            case "<":
                jet_delta = Pos(-1, 0)
        after_jet = [tile + jet_delta for tile in self.falling]
        if not self._collision(after_jet):
            self.falling = after_jet

        fall_delta = Pos(0, -1)
        after_fall = [tile + fall_delta for tile in self.falling]
        if not self._collision(after_fall):
            self.falling = after_fall
        else:
            for pos in self.falling:
                self.chamber[pos.y][pos.x] = "#"
            self.falling = []
            self.stopped_rocks += 1

    def _spawn(self):
        rock = [list(row) for row in next(self.rock_queue)[1]]

        empty = len(self.chamber) - self._height_current
        space_needed = 3 + len(rock) - empty
        y_origin = len(self.chamber) - 1 + space_needed

        self.chamber.extend(list(EMPTY_ROW) for _ in range(space_needed))

        self.falling = []
        for y, row in enumerate(rock):
            for x, tile in enumerate(row):
                if tile == "@":
                    self.falling.append(Pos(x, y_origin - y))

    def _collision(self, tiles: Iterable[Pos]) -> bool:
        for tile in tiles:
            inside = tile.y >= 0 and 0 <= tile.x < WIDTH  # tile never moves up
            if not inside or self.chamber[tile.y][tile.x] == "#":
                return True
        return False

    def __str__(self):
        res = []
        for y in reversed(range(len(self.chamber))):
            for x in range(WIDTH):
                if Pos(x, y) in self.falling:
                    res.append("@")
                else:
                    res.append(self.chamber[y][x])
            res.append("\n")
        return "".join(res)

    def find_loop(self) -> list[int]:
        # advance the game until it enters infinite loop
        memoize = {}
        last_height = 0
        while True:
            rock_index, _ = self.rock_queue.peek()
            jet_index, _ = self.jet_queue.peek()
            memo = hash((tuple(flatten(self.chamber)), rock_index, jet_index))

            if memo not in memoize:
                self.round()
                self._trim()
                memoize[memo] = self.height - last_height
                last_height = self.height
                continue

            # dicts keep insertion order
            loop_start = next(i for i, key in enumerate(memoize) if key == memo)
            return [delta for delta in list(memoize.values())[loop_start:]]

    def _trim(self):
        cols = list(zip(*self.chamber))
        try:
            stopped_lowest = max(col[::-1].index("#") for col in cols)
            self._height_base += len(self.chamber) - 1 - stopped_lowest
            self.chamber = self.chamber[-stopped_lowest - 1 :]
        except ValueError:
            return


def part_1(s: str) -> int:
    game = Game(s)
    for _ in range(2022):
        game.round()
    return game.height


def part_2(s: str) -> int:
    rounds = 1_000_000_000_000

    game = Game(s)
    loop = game.find_loop()
    rounds_left = rounds - game.stopped_rocks

    full_loops = rounds_left // len(loop)
    rem_loop = rounds_left % len(loop)
    return game.height + full_loops * sum(loop) + sum(loop[:rem_loop])


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
