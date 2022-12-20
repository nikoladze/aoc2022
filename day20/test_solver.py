import logging
import pytest
from solver import parse, solve1, solve2, logger, move_entry
from collections import deque


TESTDATA = """
1
2
-3
3
-2
0
4
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA.strip())


def test_parse(parsed_data):
    data = parsed_data
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    solution = solve1(parsed_data)
    assert solution == 3


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here

def equal_up_to_rotation(l1, l2):
    d2 = deque(l2)
    for i in l1:
        if l1 == list(d2):
            return True
        d2.rotate()
    return False

def test_move():
    l = [1, 2, 3]
    move_entry(l, 0, 1)
    assert equal_up_to_rotation(l, [2, 1, 3])
