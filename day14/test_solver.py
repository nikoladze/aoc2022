from pathlib import Path
import pytest
from solver import parse, solve1, solve2

TESTDATA = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA.strip())


def test_parse():
    data = parse(TESTDATA.strip())
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 24

# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 93


def test_solution():
    data = parse(open(Path(__file__).parent / "input.txt").read())
    assert solve1(data) == 808
    assert solve2(data) == 26625
