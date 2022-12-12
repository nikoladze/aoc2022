#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def get_pos(data, letter):
    for j, row in enumerate(data):
        for i, v in enumerate(row):
            if v == letter:
                return (i, j)


def elevation(letter):
    if letter == "S":
        return ord("a")
    if letter == "E":
        return ord("z")
    return ord(letter)


CACHE = {}


def get_cost_map(data):
    cache_key = tuple(data)
    if cache_key in CACHE:
        return CACHE[cache_key]

    i, j = get_pos(data, "E")
    costs = [[None for _ in row] for row in data]
    costs[j][i] = 0
    elevation_map = [[elevation(letter) for letter in row] for row in data]

    nrows = len(data)
    ncols = len(data[0])

    def search_from(i, j):
        prev = elevation_map[j][i]
        cost = costs[j][i]
        for dx, dy in [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]:
            new_i, new_j = i + dx, j + dy
            if new_i < 0 or new_j < 0 or new_i >= ncols or new_j >= nrows:
                continue
            new_cost = cost + 1
            other_cost = costs[new_j][new_i]
            if other_cost is not None and other_cost <= new_cost:
                continue
            new = elevation_map[new_j][new_i]
            if (prev - new) > 1:
                continue
            costs[new_j][new_i] = new_cost
            search_from(new_i, new_j)

    search_from(i, j)
    CACHE[cache_key] = costs
    return costs


# PART 1
@measure_time
def solve1(data):
    costs = get_cost_map(data)
    i, j = get_pos(data, "S")
    return costs[j][i]


# PART 2
@measure_time
def solve2(data):
    costs = get_cost_map(data)
    return min(
        min(
            cost
            for i, cost in enumerate(row)
            if cost is not None and data[j][i] in ["a", "S"]
        )
        for j, row in enumerate(costs)
    )


if __name__ == "__main__":
    # need slightly more than the default ;)
    sys.setrecursionlimit(3000)

    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
