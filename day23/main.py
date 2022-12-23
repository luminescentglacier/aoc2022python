# --- Day 23: Unstable Diffusion ---
from collections import Counter, deque
from dataclasses import dataclass
from enum import Enum
from itertools import count
from pathlib import Path
from typing import Self

INPUT_FILE = Path(__file__).parent / "input.txt"


@dataclass(unsafe_hash=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Pos(self.x + other.x, self.y + other.y)


class Dir(Enum):
    N = Pos(0, -1)
    S = Pos(0, 1)
    W = Pos(-1, 0)
    E = Pos(1, 0)

    NW = Pos(-1, -1)
    NE = Pos(1, -1)
    SW = Pos(-1, 1)
    SE = Pos(1, 1)

    def adjacent(self, center: Pos) -> list[Pos]:
        match self:
            case self.N:
                dirs = [self.N, self.NE, self.NW]
            case self.S:
                dirs = [self.S, self.SE, self.SW]
            case self.W:
                dirs = [self.W, self.NW, self.SW]
            case self.E:
                dirs = [self.E, self.NE, self.SE]
            case _:
                raise NotImplementedError
        return [center + d.value for d in dirs]


@dataclass
class Elf:
    pos: Pos
    proposal: Pos | None = None


class Game:
    elfs: dict[Pos, Elf]
    move_queue: deque[Dir]

    def __init__(self, elfs: dict[Pos, Elf]) -> None:
        self.elfs = elfs
        self.move_queue = deque((Dir.N, Dir.S, Dir.W, Dir.E))

    @classmethod
    def parse(cls, s: str) -> Self:
        elfs = {}
        for y, line in enumerate(s.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    elf = Elf(Pos(x, y))
                    elfs[elf.pos] = elf
        return cls(elfs)

    def tick(self):
        # propose
        for elf in self.elfs.values():
            elf.proposal = None

            if not self.get_neighbours(elf):
                continue

            for direction in self.move_queue:
                if not any(adj in self.elfs for adj in direction.adjacent(elf.pos)):
                    elf.proposal = elf.pos + direction.value
                    break

        # move
        proposals = Counter(elf.proposal for elf in self.elfs.values() if elf.proposal)
        if not proposals:
            raise RuntimeError("All elfs are spread out!")

        new_elfs = {}
        for elf in self.elfs.values():
            if proposals[elf.proposal] == 1:
                elf.pos = elf.proposal
            new_elfs[elf.pos] = elf

        self.elfs = new_elfs
        self.move_queue.rotate(-1)

    def get_neighbours(self, elf: Elf) -> list[Elf]:
        candidates = [elf.pos + d.value for d in Dir]
        return [n for pos in candidates if (n := self.elfs.get(pos))]

    def rectangle(self) -> tuple[int, int, int, int]:
        positions = self.elfs.keys()
        l = min(positions, key=lambda p: p.x)
        r = max(positions, key=lambda p: p.x)
        u = min(positions, key=lambda p: p.y)
        d = max(positions, key=lambda p: p.y)
        return l.x, u.y, r.x, d.y

    def empty_tiles(self) -> int:
        l, u, r, d = self.rectangle()
        area = (r - l + 1) * (d - u + 1)
        return area - len(self.elfs)

    def __str__(self) -> str:
        res = []
        l, u, r, d = self.rectangle()
        for y in range(u - 1, d + 2):
            for x in range(l - 1, r + 2):
                res.append("#" if self.elfs.get(Pos(x, y)) else ".")
            res.append("\n")
        return "".join(res)


def part_1(s: str) -> int:
    game = Game.parse(s)
    for _ in range(1, 11):
        game.tick()
    return game.empty_tiles()


def part_2(s: str) -> int:
    game = Game.parse(s)
    for i in count(1):
        try:
            game.tick()
        except RuntimeError:
            return i


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
