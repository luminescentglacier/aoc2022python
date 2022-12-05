from pathlib import Path


def initial_positions(s: str) -> list[list[str]]:
    for i, line in enumerate(s.splitlines()):
        if line.startswith(" 1"):
            stacks_num = int(line.split()[-1])
            index_row = i
            break
    else:
        raise ValueError("Unable to find crates number")

    stacks = [[] for _ in range(stacks_num)]
    for line in s.splitlines()[:index_row]:
        for i, crate in enumerate(line[1::4]):
            if crate != " ":
                stacks[i].insert(0, crate)
    return stacks


def instructions(s: str) -> tuple[int, int, int]:
    for line in s.splitlines():
        if not line.startswith("move"):
            continue
        words = line.split()
        count, src, dst = int(words[1]), int(words[3]) - 1, int(words[5]) - 1
        yield count, src, dst


def part_1(s: str) -> str:
    stacks = initial_positions(s)
    for count, src, dst in instructions(s):
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())
    return "".join(s[-1] for s in stacks)


def part_2(s: str) -> str:
    stacks = initial_positions(s)
    for count, src, dst in instructions(s):
        stacks[dst].extend(stacks[src][-count:])
        stacks[src] = stacks[src][:-count]
    return "".join(s[-1] for s in stacks)


if __name__ == "__main__":
    s = Path("input.txt").read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
