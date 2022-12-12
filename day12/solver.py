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


# PART 1
@measure_time
def solve1(data):
    start = get_pos(data, "S")
    costs = {start: 0}

    def search_from(pos):
        i, j = pos
        prev = elevation(data[j][i])
        cost = costs[pos]
        for dx, dy in [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]:
            new_pos = (i + dx, j + dy)
            if not (
                (0 <= new_pos[0] < len(data[0])) and (0 <= new_pos[1] < len(data))
            ):
                continue
            letter = data[new_pos[1]][new_pos[0]]
            new = elevation(letter)
            #print(f"{pos=}, {new_pos=}, {new=}, {cost=}")
            if (new - prev) > 1:
                continue
            if new_pos in costs and costs[new_pos] <= (cost + 1):
                continue
            costs[new_pos] = cost + 1
            if letter == "E":
                continue
            search_from(new_pos)

    res =  search_from(start)
    end = get_pos(data, "E")
    return costs[end]


# PART 2
@measure_time
def solve2(data):
    start = get_pos(data, "E")
    costs = {start: 0}

    def search_from(pos):
        i, j = pos
        prev = elevation(data[j][i])
        cost = costs[pos]
        for dx, dy in [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]:
            new_pos = (i + dx, j + dy)
            if not (
                (0 <= new_pos[0] < len(data[0])) and (0 <= new_pos[1] < len(data))
            ):
                continue
            letter = data[new_pos[1]][new_pos[0]]
            new = elevation(letter)
            #print(f"{pos=}, {new_pos=}, {new=}, {cost=}")
            if (prev - new) > 1:
                continue
            if new_pos in costs and costs[new_pos] <= (cost + 1):
                continue
            costs[new_pos] = cost + 1
            if letter == "a":
                continue
            search_from(new_pos)

    res =  search_from(start)
    #end = get_pos(data, "E")
    #return costs[end]
    return min(cost for pos, cost in costs.items() if elevation(data[pos[1]][pos[0]]) == ord("a"))


if __name__ == "__main__":

    import resource, sys
    resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
    sys.setrecursionlimit(10**6)

    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
