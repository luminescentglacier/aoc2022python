from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Iterable, Self

INPUT_FILE = Path(__file__).parent / "input.txt"


@dataclass
class Dir:
    name: str
    parent: Self
    files: dict[str, int] = field(default_factory=dict)
    dirs: dict[str, Self] = field(default_factory=dict)

    @cached_property
    def size(self) -> int:
        # size is only called after inserting all the nodes, so no need for invalidation logic
        return sum(self.files.values()) + sum(d.size for d in self.dirs.values())

    def dfs(self) -> Iterable[Self]:
        for dir in self.dirs.values():
            yield from dir.dfs()
        yield self


def parse_fs(s: str) -> Dir:
    root = Dir(name="/", parent=None)  # type: ignore
    pwd = root

    for entry in s.split("$ ")[1:]:
        command, *output = entry.splitlines()
        match command.split():
            case "cd", subdir:
                match subdir:
                    case "/":
                        pwd = root
                    case "..":
                        pwd = pwd.parent
                    case subdir:
                        if subdir not in pwd.dirs:
                            pwd.dirs[subdir] = Dir(name=subdir, parent=pwd)
                        pwd = pwd.dirs[subdir]

            case ["ls"]:
                for line in output:
                    match line.split(maxsplit=1):
                        case "dir", subdir:
                            if subdir not in pwd.dirs:
                                pwd.dirs[subdir] = Dir(name=subdir, parent=pwd)
                        case size, file:
                            if file not in pwd.files:
                                pwd.files[file] = int(size)

            case cmd:
                raise ValueError(f"Unknown command {cmd}")
    return root


def part_1(s: str) -> int:
    root = parse_fs(s)
    score = 0
    for dir in root.dfs():
        if dir.size < 100_000:
            score += dir.size
    return score


def part_2(s: str) -> int:
    MEM_MAX = 70000000
    UPDATE_SIZE = 30000000

    root = parse_fs(s)
    free = MEM_MAX - root.size
    to_free = UPDATE_SIZE - free

    candidates = sorted(d.size for d in root.dfs())
    return next(c for c in candidates if c > to_free)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
