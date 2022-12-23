import pytest
from solver import parse, solve1, solve2, Cube
from testdata import TESTDATA, TEST_AREAS, TEST_CONNECTIONS

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
    solution = solve2(parsed_data, areas=TEST_AREAS, connections=TEST_CONNECTIONS)
    assert solution == 5031


@pytest.mark.parametrize(
    "before,after",
    [
        ((11, 6, 1, 0), (13, 8, 0, 1)),
        ((8, 0, 0, -1), (3, 4, 0, 1)),
        ((8, 0, -1, 0), (4, 4, 0, 1)),
        ((10, 3, 0, 1), (10, 4, 0, 1)),
    ]
)
def test_wrapped(parsed_data, before, after):
    grid, instructions = parsed_data
    cube = Cube(grid, areas=TEST_AREAS, connections=TEST_CONNECTIONS)
    assert cube.wrapped(*before) == after
