#!/usr/bin/env python

import sys
from pathlib import Path
from functools import reduce
from operator import mul

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [[int(i) for i in line] for line in raw_data.strip().splitlines()]


def print_visible(data, visible):
    ncols = len(data[0])
    nrows = len(data)
    for j in range(nrows):
        for i in range(ncols):
            height = data[j][i]
            if visible[j][i]:
                print("\033[1m" + str(height) + "\033[0m", end="")
            else:
                print(height, end="")
        print("")


def get_visible(data):
    ncols = len(data[0])
    nrows = len(data)
    visible = [[False for i in row] for row in data]
    for get_ij, range_x, range_y in [
        (lambda x, y: (y, x), range(nrows), range(ncols)),
        (lambda x, y: (y, x), range(nrows), range(ncols - 1, -1, -1)),
        (lambda x, y: (x, y), range(ncols), range(nrows)),
        (lambda x, y: (x, y), range(ncols), range(nrows - 1, -1, -1)),
    ]:
        for x in range_x:
            prev = None
            for y in range_y:
                i, j = get_ij(x, y)
                if prev is None:
                    prev = data[j][i]
                    visible[j][i] = True
                    continue
                height = data[j][i]
                if height > prev:
                    visible[j][i] = True
                    prev = height
    return visible


# PART 1
@measure_time
def solve1(data):
    visible = get_visible(data)
    return sum(sum(row) for row in visible)


# Part 2
@measure_time
def solve2(data):
    ncols = len(data[0])
    nrows = len(data)

    def nvisible_from(i, j, dx, dy):
        this_height = data[j][i]
        n = 0
        while True:
            i += dx
            j += dy
            if not (0 <= i < nrows and 0 <= j < ncols):
                return n
            other_height = data[j][i]
            n += 1
            if other_height >= this_height:
                return n

    seen_from = []
    for j in range(nrows):
        row = []
        for i in range(ncols):
            col = []
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                col.append(nvisible_from(i, j, dx, dy))
            row.append(col)
        seen_from.append(row)

    return max(max(reduce(mul, seen) for seen in row) for row in seen_from)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
