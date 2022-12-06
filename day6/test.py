import pytest
from pathlib import Path

from main import part_1, part_1_optimized, part_2, part_2_optimized


@pytest.fixture
def puzzle_input():
    return Path("test.txt").read_text()


def test_part_1(puzzle_input):
    assert part_1(puzzle_input) == 7
    assert part_1_optimized(puzzle_input) == 7


def test_part_2(puzzle_input):
    assert part_2(puzzle_input) == 19
    assert part_2_optimized(puzzle_input) == 19
