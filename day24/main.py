# --- Day 24: Blizzard Basin ---
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import count
from pathlib import Path
from typing import Self

import networkx as nx
from more_itertools import flatten

INPUT_FILE = Path(__file__).parent / "input.txt"


@dataclass(frozen=True)
class Pos:
    x: int
    y: int
    tick: int

    def __add__(self, other: Self) -> Self:
        return Pos(self.x + other.x, self.y + other.y, self.tick)


class Dir(Enum):
    Down = Pos(0, 1, tick=0)
    Up = Pos(0, -1, tick=0)
    Left = Pos(-1, 0, tick=0)
    Right = Pos(1, 0, tick=0)

    @classmethod
    def from_str(cls, s: str):
        match s:
            case ">":
                return cls.Right
            case "<":
                return cls.Left
            case "^":
                return cls.Up
            case "v":
                return cls.Down
        raise NotImplementedError

    def __str__(self):
        match self:
            case self.Right:
                return ">"
            case self.Left:
                return "<"
            case self.Up:
                return "^"
            case self.Down:
                return "v"
        raise NotImplementedError


@dataclass
class Blizzard:
    pos: Pos
    direction: Dir


@dataclass
class Valley:
    blizzards: defaultdict[Pos, list[Blizzard]]
    width: int
    height: int
    start: Pos
    end: Pos
    tick: int

    @classmethod
    def parse(cls, s: str) -> Self:
        lines = s.splitlines()

        blizzards = defaultdict(list)
        for y, line in enumerate(lines[1:-1]):
            for x, c in enumerate(line[1:-1]):
                if c != ".":
                    bliz = Blizzard(Pos(x, y, tick=0), Dir.from_str(c))
                    blizzards[bliz.pos].append(bliz)

        width = len(lines[0]) - 2
        height = len(lines) - 2
        tick = 0

        return cls(
            blizzards,
            width,
            height,
            start=Pos(0, -1, tick),
            end=Pos(width - 1, height, tick),
            tick=tick,
        )

    def build_graph(self) -> nx.Graph:
        g = nx.DiGraph()
        g.add_nodes_from((self.start, self.end))
        for y in range(self.height):
            for x in range(self.width):
                if (pos := Pos(x, y, self.tick)) not in self.blizzards:
                    g.add_node(pos)
        return g

    def connect_in_time(self, g: nx.DiGraph) -> None:
        nodes_prev = [n for n in g.nodes if n.tick == self.tick - 1]
        g_new = self.build_graph()

        for old in nodes_prev:
            new = Pos(old.x, old.y, self.tick)
            new_neighbours = [new + d.value for d in Dir]
            for node in new, *new_neighbours:
                if node in g_new:
                    g.add_edge(old, node)

    def advance(self):
        self.tick += 1
        self.start = Pos(self.start.x, self.start.y, self.tick)
        self.end = Pos(self.end.x, self.end.y, self.tick)

        new_blizzards = defaultdict(list)
        for bliz in flatten(self.blizzards.values()):
            pos = bliz.pos + bliz.direction.value
            match pos.x:
                case self.width:
                    x = 0
                case -1:
                    x = self.width - 1
                case _:
                    x = pos.x
            match pos.y:
                case self.height:
                    y = 0
                case -1:
                    y = self.height - 1
                case _:
                    y = pos.y
            bliz.pos = Pos(x, y, self.tick)
            new_blizzards[bliz.pos].append(bliz)
        self.blizzards = new_blizzards

    def __str__(self):
        res = []
        for y in range(-1, self.height + 1):
            for x in range(-1, self.width + 1):
                pos = Pos(x, y, self.tick)
                if pos == self.start or pos == self.end:
                    res.append(".")
                elif x == -1 or x == self.width or y == -1 or y == self.height:
                    res.append("#")
                elif bliz_at_pos := self.blizzards.get(pos):
                    if len(bliz_at_pos) == 1:
                        res.append(str(bliz_at_pos[0].direction))
                    else:
                        res.append(str(len(bliz_at_pos)))
                else:
                    res.append(".")
            res.append("\n")
        return "".join(res)


def part_1(s: str) -> int:
    valley = Valley.parse(s)
    g = nx.DiGraph()  # time does not flow backwards :C
    g.add_node(valley.start)

    for minute in count(1):
        valley.advance()
        valley.connect_in_time(g)
        if valley.end in g:
            return minute


def part_2(s: str) -> int:
    valley = Valley.parse(s)
    g = nx.DiGraph()
    g.add_node(valley.start)

    goals = ["E", "S", "E"]

    minute = 0
    while goals:
        minute += 1
        valley.advance()
        valley.connect_in_time(g)

        goal = valley.end if goals[0] == "E" else valley.start
        if goal in g:
            g = nx.DiGraph()  # we only need time, not full path
            g.add_node(goal)
            goals.pop(0)

    return minute


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
