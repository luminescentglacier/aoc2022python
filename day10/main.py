from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

INPUT_FILE = Path(__file__).parent / "input.txt"


def chunks(iterable: Iterable[str], size: int) -> Iterable[tuple[str, ...]]:
    args = [iter(iterable)] * size
    return zip(*args, strict=True)


def instructions(s: str) -> Iterable[tuple[str, list[int]]]:
    for line in s.splitlines():
        cmd, *arg = line.split(maxsplit=1)
        yield cmd, list(map(int, arg))


@dataclass
class CPU:
    reg_x: int = 1
    cycle: int = 0

    def draw(self) -> str:
        if self.reg_x - 1 <= (self.cycle - 1) % 40 <= self.reg_x + 1:
            return "#"
        return "."

    def process(self, cmd: str, args: list[int]) -> Iterable[str]:
        match cmd, args:
            case "noop", []:
                self.cycle += 1
                yield self.draw()
            case "addx", [val]:
                for _ in range(2):
                    self.cycle += 1
                    yield self.draw()
                self.reg_x += val
            case _:
                raise ValueError(f"Invalid cmd {cmd} {args}")


def part_1(s: str) -> int:
    cpu = CPU()
    signal = 0
    for cmd, args in instructions(s):
        for _ in cpu.process(cmd, args):
            if (cpu.cycle + 20) % 40 == 0:
                signal += cpu.cycle * cpu.reg_x
    return signal


def part_2(s: str) -> str:
    cpu = CPU()
    pixels = []
    for cmd, args in instructions(s):
        pixels.extend(cpu.process(cmd, args))
    return "".join(pixels)


def crt(pixels: str) -> str:
    rows = ("".join(c) for c in chunks(pixels, 40))
    return "\n".join(rows)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2:\n{crt(part_2(s))}")
