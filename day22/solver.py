#!/usr/bin/env python

import sys
from pathlib import Path
from collections import deque

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    grid, pw = raw_data.split("\n\n")
    grid = grid.splitlines()
    instructions = []
    start = 0
    pos = 0
    while pos < len(pw):
        if pw[pos] in "LR":
            if start != pos:
                instructions.append(int(pw[start:pos]))
            instructions.append(pw[pos])
            start = pos + 1
        pos += 1
    if start != pos:
        instructions.append(int(pw[start:pos]))
    return grid, instructions


def print_grid(grid, x, y):
    grid = [list(row) for row in grid]
    grid[y][x] = "o"
    print("\n".join(["".join(row) for row in grid]))


# PART 1
@measure_time
def solve1(data):
    grid, instructions = data
    facings = deque([0, 1, 2, 3])
    facing = facings[0]
    for i, c in enumerate(grid[0]):
        if c == ".":
            x, y = (i, 0)
            break

    def in_grid(x, y):
        if x < 0 or y < 0:
            return False
        try:
            c = grid[y][x]
        except IndexError:
            return False
        if c == " ":
            return False
        return True

    def wrap(x, y, dx, dy):
        while True:
            x2, y2 = x - dx, y - dy
            if not in_grid(x2, y2):
                return x, y
            x, y = x2, y2

    # print()
    # print_grid(grid, x, y)
    for instruction in instructions:
        # print()
        # print(f"{instruction=}, {facings[0]=}")
        # print()
        if instruction == "L":
            facings.rotate(1)
        elif instruction == "R":
            facings.rotate(-1)
        else:
            facing = facings[0]
            dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][facing]
            for i in range(instruction):
                # print(f"{dx=}, {dy=}")
                x2, y2 = (x + dx, y + dy)
                if not in_grid(x2, y2):
                    x2, y2 = wrap(x2, y2, dx, dy)
                    # print("wrapping to:")
                    # print_grid(grid, x2, y2)
                # print(f"{x=}, {y=}, {x2=}, {y2=}")
                # print(f"{grid[y][x]=}, {grid[y2][x2]=}")
                if grid[y2][x2] == "#":
                    # print("hit the wall - done moving")
                    break
                x, y = x2, y2
                #input()
                #print_grid(grid, x, y)

    row = y + 1
    col = x + 1
    return 1000 * row + 4 * col + facing


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
