from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from . import main
from .main import part_1, part_2

TEST_INPUT_FILE = Path(__file__).parent / "test.txt"
TEST_Y = 10


@pytest.fixture
def puzzle_input(mocker: MockerFixture):
    mocker.patch.object(main, "Y", TEST_Y)
    return TEST_INPUT_FILE.read_text()


def test_part_1(puzzle_input):
    assert part_1(puzzle_input) == 26


def test_part_2(puzzle_input):
    assert part_2(puzzle_input) == 56000011
