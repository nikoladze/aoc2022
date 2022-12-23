#!/usr/bin/env python

import sys
from pathlib import Path
from collections import defaultdict, deque

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.splitlines()


def print_grid(positions):
    xs = [x for x, y in positions]
    ys = [y for x, y in positions]
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if (x, y) in positions:
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")


def solve(data, max_rounds=10000, trace=None):
    positions = set()
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == "#":
                positions.add((x, y))

    directions = deque(
        [
            ((0, -1), ((-1, -1), (0, -1), (1, -1))),
            ((0, 1), ((-1, 1), (0, 1), (1, 1))),
            ((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),
            ((1, 0), ((1, -1), (1, 0), (1, 1))),
        ]
    )

    def no_one_else_around(x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if (x + dx, y + dy) in positions:
                    return False
        return True

    prev = positions.copy()
    if trace is not None:
        trace.append(frozenset(positions))
    for round in range(max_rounds):
        proposed = defaultdict(list)
        for x, y in positions:
            if no_one_else_around(x, y):
                continue
            for (prop_dx, prop_dy), check_directions in directions:
                if not any((x + dx, y + dy) in positions for dx, dy in check_directions):
                    proposed[(x + prop_dx, y + prop_dy)].append((x, y))
                    break
        for (x_new, y_new), orig in proposed.items():
            if len(orig) > 1:
                continue
            x, y = orig[0]
            positions.remove((x, y))
            positions.add((x_new, y_new))
        directions.rotate(-1)
        if prev == positions:
            return round + 1, positions
        prev = positions.copy()
        if trace is not None:
            trace.append(frozenset(positions))

    return None, positions


# PART 1
@measure_time
def solve1(data):
    _, positions = solve(data, max_rounds=10)

    xs = [x for x, y in positions]
    ys = [y for x, y in positions]
    total = 0
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if not (x, y) in positions:
                total += 1
    return total


# PART 2
@measure_time
def solve2(data):
    return solve(data, max_rounds=10000)[0]


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
