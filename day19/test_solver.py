import pytest
from solver import parse, solve1, solve2

TESTDATA = """
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
"""

TESTDATA = "\n".join(
    " ".join(line.strip() for line in block.splitlines())
    for block in TESTDATA.strip().split("\n\n")
)


@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    # 9 + 2 * 12
    assert solution == 33


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # 56 * 62 = 3472
    assert solution == 3472
