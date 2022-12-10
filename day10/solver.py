#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def generate_values(data):
    x = 1
    i = 1
    result = 0
    for line in data:
        tokens = line.split()
        if len(tokens) == 1:
            yield i, x
            i += 1
            continue
        v = int(tokens[1])
        yield i, x
        i += 1
        yield i, x
        i += 1
        x += v


# PART 1
@measure_time
def solve1(data):
    result = 0
    for i, v in generate_values(data):
        if i in [20, 60, 100, 140, 180, 220]:
            result += i * v
    return result


# PART 2
@measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

