import pytest
from solver import parse, solve1, solve2

TESTDATA = """
30373
25512
65332
33549
35390
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
    assert solution == 21


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 8
