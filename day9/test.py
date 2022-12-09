from pathlib import Path

import pytest

from .main import part_1, part_2

P1_TEST_INPUT_FILE = Path(__file__).parent / "test.txt"
P2_TEST_INPUT_FILE = Path(__file__).parent / "test_2.txt"


def test_part_1():
    assert part_1(P1_TEST_INPUT_FILE.read_text()) == 13


def test_part_2():
    assert part_2(P2_TEST_INPUT_FILE.read_text()) == 36
