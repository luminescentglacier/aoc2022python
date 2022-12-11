from functools import partial
from itertools import takewhile
from operator import mul
from pathlib import Path
from pprint import pprint

import numpy as np

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str) -> list[list[int]]:
    return [list(map(int, l)) for l in s.splitlines()]


def part_1(s: str) -> int:
    grid = np.array(parse(s))
    return visible(grid).sum()


def visible(grid) -> np.ndarray:
    mask = np.full_like(grid, False)
    for _ in range(4):
        view(grid, mask)
        grid, mask = map(np.rot90, (grid, mask))
    return mask


def view(grid, visible):
    for row, mask in zip(grid, visible):
        highest = -1
        for i, tree in enumerate(row):
            if tree > highest:
                highest = tree
                mask[i] = True


def part_2(s: str) -> int:
    grid = np.array(parse(s))
    scores = np.zeros_like(grid, dtype="4int")
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            scores[row][col] = score(grid, row, col)
    return np.product(scores, axis=2).max()


def score(grid, y, x) -> np.ndarray:
    house = grid[y][x]
    col, row = grid[:, x], grid[y]
    left, right = row[:x][::-1], row[x + 1 :]
    up, down = col[:y][::-1], col[y + 1 :]
    return np.array([trees_visible(d, house) for d in (up, left, right, down)])


def trees_visible(direction: np.ndarray, house: int) -> int:
    total = 0
    for tree in direction:
        total += 1
        if tree >= house:
            break
    return total


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
