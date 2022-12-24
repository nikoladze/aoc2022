#!/usr/bin/env python

import sys
from pathlib import Path
from collections import defaultdict, deque
from copy import deepcopy

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.splitlines()


def print_grid(blizzards, wall, nrows, ncols):
    print()
    for y in range(nrows):
        for x in range(ncols):
            if (x, y) in wall:
                print("#", end="")
                continue
            tile_blizzards = blizzards[x, y]
            if len(tile_blizzards) == 0:
                print(".", end="")
                continue
            if len(tile_blizzards) > 1:
                print(len(tile_blizzards), end="")
                continue
            print(next(iter(tile_blizzards)), end="")
        print("\n", end="")


MAX_T = 1000


def search(data, start, goal, t=0):
    blizzards = defaultdict(set)
    blizzards_row_col = {k: defaultdict(list) for k in "<>^v"}

    wall = set()
    nrows = len(data)
    ncols = len(data[-1])
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == "#":
                wall.add((x, y))
                continue
            if c != ".":
                blizzards[x, y].add(c)
                # coordinates here w/o walls
                if c in "<>":
                    blizzards_row_col[c][y - 1].append(x - 1)
                if c in "^v":
                    blizzards_row_col[c][x - 1].append(y - 1)
                continue

    def is_hit_at(x, y, t):
        # w/o walls
        nc = ncols - 2
        nr = nrows - 2
        x -= 1
        y -= 1
        for xb in blizzards_row_col[">"][y]:
            if (xb + t) % nc == x:
                return True
        for xb in blizzards_row_col["<"][y]:
            if (xb - t) % nc == x:
                return True
        for yb in blizzards_row_col["v"][x]:
            if (yb + t) % nr == y:
                return True
        for yb in blizzards_row_col["^"][x]:
            if (yb - t) % nr == y:
                return True
        return False

    def is_outside(x, y):
        if x < 0 or y < 0:
            return True
        if x >= ncols or y >= nrows:
            return True
        return False

    def search(start, goal, t):
        x, y = start
        times = set([MAX_T])
        visited = set()
        q = [(x, y, t)]
        while q:
            x, y, t = q.pop()
            if (x, y) == goal:
                times.add(t)
            visited.add((x, y, t))
            min_t = min(times)
            # order: first try right, left, stop, ...
            for dx, dy in [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)]:
                xnew, ynew = x + dx, y + dy
                tnew = t + 1
                if (xnew, ynew) in wall:
                    continue
                if tnew >= min_t:
                    continue
                if (xnew, ynew, tnew) in visited:
                    continue
                if is_outside(xnew, ynew):
                    continue
                if is_hit_at(xnew, ynew, tnew):
                    continue
                q.append((xnew, ynew, tnew))
        return min(times)

    return search(start, goal, t=t)


# PART 1
@measure_time
def solve1(data):
    nrows = len(data)
    ncols = len(data[-1])
    return search(data, start=(1, 0), goal=(ncols - 2, nrows - 1))


# PART 2
@measure_time
def solve2(data):
    nrows = len(data)
    ncols = len(data[-1])
    start = (1, 0)
    goal = (ncols - 2, nrows - 1)
    t1 = search(data, start=start, goal=goal)
    t2 = search(data, start=goal, goal=start, t=t1)
    t3 = search(data, start=start, goal=goal, t=t2)
    return t3


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
