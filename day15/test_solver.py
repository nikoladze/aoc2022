import pytest
from solver import parse, solve1, solve2, find_not_covered

TESTDATA = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA.strip())


def test_parse():
    data = parse(TESTDATA.strip())
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data, where_y=10)
    assert solution == 26


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data, ymax=20)
    assert solution == 56000011


def test_not_covered():
    assert find_not_covered([(0, 10), (20, 25)], 8, 30) == [(11, 19), (26, 30)]
    assert find_not_covered([(-1, 5)], 0, 10) == [(6, 10)]
    assert find_not_covered([(2, 5)], 0, 10) == [(0, 1), (6, 10)]
    assert find_not_covered([(5, 15)], 0, 10) == [(0, 4)]
    assert find_not_covered([(-1, 11)], 0, 10) == []
    assert find_not_covered([(-30, -20)], 0, 10) == [(0, 10)]
    assert find_not_covered([(5, 5)], 0, 10) == [(0, 4), (6, 10)]
    assert find_not_covered([(-3, 5), (7, 12)], 0, 10) == [(6, 6)]
    assert find_not_covered([(-3, 0)], 0, 10) == [(1, 10)]
    assert find_not_covered([(10, 15)], 0, 10) == [(0, 9)]
    assert find_not_covered([(10, 15)], 10, 10) == []
    assert find_not_covered([(-10, 5), (20, 30), (40, 50), (60, 70), (88, 88), (90, 110)], 0, 100) == [(6, 19), (31, 39), (51, 59), (71, 87), (89, 89)]
    assert find_not_covered([(-10, 50), (92, 200), (40, 70), (50, 90)], 0, 100) == [(91, 91)]
