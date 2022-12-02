import pytest
from pathlib import Path

from main import part_1, part_2


@pytest.fixture
def test_input():
    return Path("test.txt").read_text()


def test_part_1(test_input):
    assert part_1(test_input) == 15


def test_part_2(test_input):
    assert part_2(test_input) == 12
