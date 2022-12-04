#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [
        [[int(i) for i in range.split("-")] for range in line.split(",")]
        for line in raw_data.splitlines()
    ]


# PART 1
@measure_time
def solve1(data):
    return sum(((a1 - b1) * (a2 - b2)) <= 0 for (a1, a2), (b1, b2) in data)


def overlaps(r1, r2):
    if r1[1] >= r2[0] and r2[0] >= r1[0]:
        return True
    return False


def contains(a1, a2, b1, b2):
    return ((a1 - b1) * (a2 - b2)) <= 0


# PART 2
@measure_time
def solve2(data):
    return sum(
        overlaps((a1, a2), (b1, b2))
        or overlaps((b1, b2), (a1, a2))
        or contains(a1, a2, b1, b2)
        for (a1, a2), (b1, b2) in data
    )


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
