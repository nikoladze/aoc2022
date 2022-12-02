import pytest
from solver import parse, solve1, solve2, solve1_alternative, solve2_alternative

TESTDATA = """
A Y
B X
C Z
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 15


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 12


def test_solve1_alternative(parsed_data):
    solution = solve1_alternative(parsed_data)
    assert solution == 15


def test_solve2_alternative(parsed_data):
    solution = solve2_alternative(parsed_data)
    assert solution == 12
