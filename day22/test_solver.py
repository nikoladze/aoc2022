import pytest
from solver import parse, solve1, solve2

TESTDATA = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""[1:-1]

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 6032


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here
