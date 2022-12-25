# --- Day 25: Full of Hot Air ---
from itertools import count
from pathlib import Path

from z3 import *

INPUT_FILE = Path(__file__).parent / "input.txt"

FROM_SNAFU = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
TO_SNAFU = {v: k for k, v in FROM_SNAFU.items()}


def from_snafu(s: str) -> int:
    return sum(FROM_SNAFU[c] * 5**i for i, c in enumerate(reversed(s)))


def to_snafu(num: int) -> str:
    res = []
    while num:
        match rem := num % 5:
            case 0 | 1 | 2:
                res.append(str(rem))
                carry = 0
            case 3:  # 5 - 2
                res.append("=")
                carry = 1
            case 4:  # 5 - 1
                res.append("-")
                carry = 1
        num = num // 5 + carry
    return "".join(res)


def to_snafu_z3(num: int) -> str:
    # kinda cool you can specify almost arbitrary constraints
    for power in count():
        s = Solver()

        res = 0
        digit_vars = []
        for i in range(power):
            d = Int(f"d_{i}")
            digit_vars.append(d)
            s.add(And(d >= -2, d <= 2))
            res += d * 5**i

        s.add(res == num)
        if str(s.check()) == "sat":
            break

    model = s.model()
    digits = [model.eval(m).as_long() for m in reversed(digit_vars)]
    return "".join(TO_SNAFU[d] for d in digits)


def part_1(raw: str) -> str:
    code = sum(from_snafu(line) for line in raw.splitlines())
    return to_snafu(code)


def part_2(s: str) -> int:
    ...


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
