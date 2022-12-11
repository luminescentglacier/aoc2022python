from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Callable, Self

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str):
    return [Monkey.parse(raw) for raw in s.split("\n\n")]


@dataclass
class Monkey:
    index: int
    queue: list[int]
    op: Callable[[int], int]
    div: int
    target_true: int
    target_false: int
    annoyance: int = 0

    @classmethod
    def parse(cls, raw: str) -> Self:
        lines = raw.splitlines()
        values = [l.split(": ")[1] for l in lines[1:]]

        match lines[2].split()[-2:]:
            case "+", "old":
                op = lambda old: old + old
            case "*", "old":
                op = lambda old: old * old
            case "+", num if num := int(num):
                op = lambda old: old + num
            case "*", num if num := int(num):
                op = lambda old: old * num
            case unknwon_op:
                raise ValueError(f"Unknown operation {unknwon_op}")

        return cls(
            index=int(lines[0].split()[1][:1]),
            queue=[int(i) for i in values[0].split(", ")],
            op=op,
            div=int(values[2].split()[-1]),
            target_true=int(values[3].split()[-1]),
            target_false=int(values[4].split()[-1]),
        )

    def get_target(self, new: int) -> int:
        return self.target_true if new % self.div == 0 else self.target_false


def part_1(s: str) -> int:
    monkeys = parse(s)
    for _ in range(20):
        for m in monkeys:
            m.annoyance += len(m.queue)
            while m.queue:
                old = m.queue.pop()
                new = m.op(old) // 3
                target = m.get_target(new)
                monkeys[target].queue.append(new)
    annoyance = sorted(m.annoyance for m in monkeys)
    return reduce(mul, annoyance[-2:])


def part_2(s: str) -> int:
    monkeys = parse(s)
    common = reduce(mul, (m.div for m in monkeys))
    for _ in range(10_000):
        for m in monkeys:
            m.annoyance += len(m.queue)
            while m.queue:
                old = m.queue.pop()
                new = m.op(old) % common
                target = m.get_target(new)
                monkeys[target].queue.append(new)
    annoyance = sorted(m.annoyance for m in monkeys)
    return reduce(mul, annoyance[-2:])


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
