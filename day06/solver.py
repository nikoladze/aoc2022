#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip()


def solve(data, n):
    for i, window in enumerate(zip(*[data[j:] for j in range(n)])):
        if len(set(window)) == n:
            return i + n


# PART 1
@measure_time
def solve1(data):
    return solve(data, 4)


# PART 2
@measure_time
def solve2(data):
    return solve(data, 14)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
