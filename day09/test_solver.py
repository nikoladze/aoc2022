import pytest
from solver import parse, solve1, solve2


TESTDATA = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

TESTDATA2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
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
    assert solution == 13


# PART 2
def test_solve2():
    solution = solve2(parse(TESTDATA2.strip()))
    assert solution == 36
