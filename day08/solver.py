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


# PART 1
@measure_time
def solve1_old(data):
    ncols = len(data[0])
    nrows = len(data)
    visible = [[False for i in row] for row in data]
    for j, row in enumerate(data):
        left = row[0]
        visible[j][0] = True
        for i, height in enumerate(row[1:], 1):
            if height > left:
                visible[j][i] = True
                left = height
        right = row[-1]
        visible[j][-1] = True
        for i in range(ncols - 2, -1, -1):
            height = data[j][i]
            if height > right:
                visible[j][i] = True
                right = height
    for i in range(ncols):
        top = data[0][i]
        visible[0][i] = True
        for j in range(1, nrows):
            height = data[j][i]
            if height > top:
                visible[j][i] = True
                top = height
        bottom = data[-1][i]
        visible[-1][i] = True
        for j in range(nrows - 2, -1, -1):
            height = data[j][i]
            if height > bottom:
                visible[j][i] = True
                bottom = height
    from pprint import pprint

    # print("\n".join(["".join([str(int(i)) for i in row]) for row in visible]))
    for j in range(nrows):
        for i in range(ncols):
            height = data[j][i]
            if visible[j][i]:
                print("\033[1m" + str(height) + "\033[0m", end="")
            else:
                print(height, end="")
        print("")
    return sum(sum(row) for row in visible)


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
    print()
    print_visible(data, visible)
    return sum(sum(row) for row in visible)


# PART 2
@measure_time
def solve2_wrong(data):
    visible = get_visible(data)

    ncols = len(data[0])
    nrows = len(data)
    seen_from = [[[0, 0, 0, 0] for i in row] for row in data]

    for i_direction, (get_ij, range_x, range_y) in enumerate(
        [
            (lambda x, y: (y, x), range(nrows), range(ncols)),
            (lambda x, y: (y, x), range(nrows), range(ncols - 1, -1, -1)),
            (lambda x, y: (x, y), range(ncols), range(nrows)),
            (lambda x, y: (x, y), range(ncols), range(nrows - 1, -1, -1)),
        ]
    ):
        for x in range_x:
            prev = None
            n = 0
            for y in range_y:
                i, j = get_ij(x, y)
                if prev is None:
                    prev = data[j][i]
                    continue
                height = data[j][i]
                if height > prev:
                    n += 1
                    seen_from[j][i][i_direction] = n
                else:
                    n = 1
                    seen_from[j][i][i_direction] = n
                if i_direction == 1 and j == 3:
                    print(n, prev, height)
                    pass
                prev = height

    for row in seen_from:
        print(row)

    return max(max(reduce(mul, seen) for seen in row) for row in seen_from)


# Part 2
@measure_time
def solve2(data):

    print_visible(data, get_visible(data))

    ncols = len(data[0])
    nrows = len(data)
    seen_from = [[[0, 0, 0, 0] for i in row] for row in data]
    for j in range(nrows):
        for i in range(ncols):
            height = data[j][i]
            for i_direction, (dx, dy) in enumerate(
                [
                    (-1, 0),
                    (1, 0),
                    (0, 1),
                    (0, -1),
                ]
            ):
                ii = i
                jj = j
                n = 0
                while True:
                    ii += dx
                    jj += dy
                    if j == 1 and i_direction == 1 and i == 2:
                        print(f"{i_direction=},{ii=},{jj=},{other=},{n=},{height=}")
                    if not (0 <= ii < nrows and 0 <= jj < ncols):
                        seen_from[j][i][i_direction] = n
                        break
                    other = data[jj][ii]
                    n += 1
                    if other >= height:
                        seen_from[j][i][i_direction] = n
                        break
    for row in seen_from:
        print(row)

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
