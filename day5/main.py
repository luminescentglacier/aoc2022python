from pathlib import Path
from typing import Iterable, Sequence


def parse(s: str) -> tuple[list[list[str]], Iterable[tuple[int, int, int]]]:
    crates_raw, instructions_raw = s.split("\n\n")
    stacks = parse_stacks(crates_raw.splitlines())
    instructions = parse_instructions(instructions_raw.splitlines())
    return stacks, instructions


def parse_stacks(lines: Sequence[str]) -> list[list[str]]:
    stacks_num = (len(lines[0]) + 1) // 4
    stacks = [[] for _ in range(stacks_num)]
    for line in lines:
        for i, crate in enumerate(line[1::4]):
            if crate != " ":
                stacks[i].insert(0, crate)
    return stacks


def parse_instructions(lines: Iterable[str]) -> Iterable[tuple[int, int, int]]:
    for line in lines:
        words = line.split()
        count, src, dst = int(words[1]), int(words[3]) - 1, int(words[5]) - 1
        yield count, src, dst


def part_1(s: str) -> str:
    stacks, instructions = parse(s)
    for count, src, dst in instructions:
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())
    return "".join(s[-1] for s in stacks)


def part_2(s: str) -> str:
    stacks, instructions = parse(s)
    for count, src, dst in instructions:
        stacks[dst].extend(stacks[src][-count:])
        stacks[src] = stacks[src][:-count]
    return "".join(s[-1] for s in stacks)


if __name__ == "__main__":
    s = Path("input.txt").read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
