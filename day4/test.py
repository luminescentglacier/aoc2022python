import pytest
from pathlib import Path

from main import part_1, part_2


@pytest.fixture
def puzzle_input():
    return Path("test.txt").read_text()


def test_part_1(puzzle_input):
    assert part_1(puzzle_input) == 2


def test_part_2(puzzle_input):
    assert part_2(puzzle_input) == 4
