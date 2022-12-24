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



# PART 1
@measure_time
def solve1(data):
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


    # evolving ...
    # for i in range(10000):
    #     prev_blizzards = deepcopy(blizzards)
    #     # print_grid(blizzards, wall, nrows, ncols)
    #     # input()
    #     for (x, y), tile_blizzards in list(blizzards.items()):
    #         for c in list(tile_blizzards):
    #             dx, dy = {
    #                 ">": (1, 0),
    #                 "<": (-1, 0),
    #                 "^": (0, -1),
    #                 "v": (0, 1),
    #             }[c]
    #             xnew, ynew = x + dx, y + dy
    #             if (xnew, ynew) in wall:
    #                 xnew, ynew = {
    #                     (1, 0): (1, y),
    #                     (-1, 0): (ncols - 2, y),
    #                     (0, -1): (x, nrows - 2),
    #                     (0, 1): (x, 1),
    #                 }[dx, dy]
    #             blizzards[x, y].remove(c)
    #             blizzards[xnew, ynew].add(c)
    #     if prev_blizzards == blizzards:
    #         print(i)

    #max_t = 693
    max_t = 688

    times = set([max_t])

    visited = set()
    x, y = (1, 0)
    t = 0
    goal = (ncols - 2, nrows - 1)
    q = deque([(x, y, t)])
    while q:
        #x, y, t = q.popleft()
        x, y, t = q.pop()
        #print(min(times), len(times))
        #print(x, y, t, len(q))
        if (x, y) == goal:
            times.add(t)
        visited.add((x, y, t))
        #for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)]:
        for dx, dy in [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)]:
        #for dx, dy in [(1, 0), (0, 1), (0, 0), (0, -1), (-1, 0)]:
            xnew, ynew = x + dx, y + dy
            tnew = t + 1
            #print(f"{xnew=}, {ynew=}, {(xnew, ynew) in wall=}, {is_outside(xnew, ynew)=}, {is_hit_at(xnew, ynew, tnew)=}")
            if (xnew, ynew) in wall:
                continue
            if is_outside(xnew, ynew):
                continue
            if is_hit_at(xnew, ynew, tnew):
                continue
            if tnew >= max_t:
                continue
            if tnew >= min(times):
                continue
            if (xnew, ynew, tnew) in visited:
                continue
            q.append((xnew, ynew, tnew))

    return min(times)


# PART 2
@measure_time
def solve2(data):
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


    #max_t = 693
    #max_t = 688

    def search(start, goal, t=0, max_t=1000):
        x, y = start
        times = set([max_t])
        visited = set()
        q = deque([(x, y, t)])
        while q:
            #x, y, t = q.popleft()
            x, y, t = q.pop()
            #print(min(times), len(times))
            #print(x, y, t, len(q))
            if (x, y) == goal:
                times.add(t)
            visited.add((x, y, t))
            #for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)]:
            for dx, dy in [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)]:
            #for dx, dy in [(1, 0), (0, 1), (0, 0), (0, -1), (-1, 0)]:
                xnew, ynew = x + dx, y + dy
                tnew = t + 1
                #print(f"{xnew=}, {ynew=}, {(xnew, ynew) in wall=}, {is_outside(xnew, ynew)=}, {is_hit_at(xnew, ynew, tnew)=}")
                if (xnew, ynew) in wall:
                    continue
                if is_outside(xnew, ynew):
                    continue
                if is_hit_at(xnew, ynew, tnew):
                    continue
                if tnew >= max_t:
                    continue
                if tnew >= min(times):
                    continue
                if (xnew, ynew, tnew) in visited:
                    continue
                q.append((xnew, ynew, tnew))

        return min(times)

    start = (1, 0)
    goal = (ncols - 2, nrows - 1)
    t1 = search(start=start, goal=goal)
    t2 = search(start=goal, goal=start, t=t1, max_t=2000)
    t3 = search(start=start, goal=goal, t=t2, max_t=3000)
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
