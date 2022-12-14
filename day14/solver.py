#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [
        [tuple(map(int, xy.split(","))) for xy in coordinates.split(" -> ")]
        for coordinates in raw_data.splitlines()
    ]


def boundaries(cave_map):
    max_x = max(x for x, y in cave_map)
    max_y = max(y for x, y in cave_map)
    min_x = min(x for x, y in cave_map)
    max_x = max(max_x, 500)
    return min_x, max_x, max_y


def print_cave(cave_map):
    min_x, max_x, max_y = boundaries(cave_map)
    for y in range(max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos in cave_map:
                print(cave_map[pos], end="")
            else:
                print(".", end="")
        print("\n", end="")


def sign(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


# PART 1
@measure_time
def solve1(data):
    cave_map = {}
    for line in data:
        for (x1, y1), (x2, y2) in zip(line, line[1:]):
            print((x1, y1), (x2, y2))
            pos = (x1, y1)
            dx = x2 - x1
            dy = y2 - y1
            while True:
                cave_map[pos] = "#"
                if pos == (x2, y2):
                    break
                pos = (pos[0] + sign(dx), pos[1] + sign(dy))


    min_x, max_x, max_y = boundaries(cave_map)

    print_cave(cave_map)

    def run():
        n = 0
        while True:
            pos = (500, 0)
            while True:
                for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
                    new_pos = (pos[0] + dx, pos[1] + dy)
                    x, y = new_pos
                    print(new_pos)
                    if x < min_x or x > max_x or y > max_y:
                        # falling forever
                        return n
                    if new_pos not in cave_map:
                        # great, i can go here
                        pos = new_pos
                        break
                else:
                    # came to halt
                    cave_map[pos] = "o"
                    n += 1
                    # print_cave(cave_map)
                    # input()
                    break

    return run()


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
