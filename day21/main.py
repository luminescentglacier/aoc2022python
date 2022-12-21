# --- Day 21: Monkey Math ---
import re
from pathlib import Path

# import antigravity
from z3 import *

INPUT_FILE = Path(__file__).parent / "input.txt"

MONKEY_RE = re.compile(r"[a-z]{4}")


def parse(s: str) -> dict[str, str]:
    monkeys = {}
    for line in s.splitlines():
        name, op = line.split(": ")
        monkeys[name] = op
    return monkeys


def part_1(s: str) -> int:
    monkeys = parse(s)
    root = monkeys["root"]
    while vars := MONKEY_RE.findall(root):
        for var in vars:
            root = root.replace(var, f"({monkeys[var]})")
    return int(eval(root))


def part_2(s: str) -> int:
    monkeys = parse(s)

    monkeys.pop("humn")
    a, _, b = monkeys["root"].split()
    root = f"{a} == {b}"

    while (vars := MONKEY_RE.findall(root)) != ["humn"]:
        for var in vars:
            if var == "humn":
                continue
            root = root.replace(var, f"({monkeys[var]})")

    s = Solver()
    humn = Int("humn")
    s.add(eval(root))
    assert s.check()
    return s.model().eval(humn)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
