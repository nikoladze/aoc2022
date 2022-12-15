#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.splitlines():
        sensor, beacon = line.split(": ")
        sensor, beacon = [s.split("at ")[1] for s in [sensor, beacon]]
        sensor, beacon = [
            tuple([int(c[2:]) for c in s.split(", ")]) for s in [sensor, beacon]
        ]
        out.append((sensor, beacon))
    return out


def print_map(data, is_not_at):
    sensors = set(sensor for sensor, beacon in data)
    beacons = set(beacon for sensor, beacon in data)
    all_points = sensors | beacons | is_not_at
    min_x = min(x for x, y in all_points)
    min_y = min(x for x, y in all_points)
    max_x = max(y for x, y in all_points)
    max_y = max(y for x, y in all_points)
    print(min_x, max_x)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos in sensors:
                print("S", end="")
            elif pos in beacons:
                print("B", end="")
            elif pos in is_not_at:
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")


from tqdm.auto import tqdm


# PART 1
@measure_time
def solve1(data, where_y=2000000):
    is_not_at = set()
    for sensor, beacon in tqdm(data):
        dx_sb = abs(sensor[0] - beacon[0])
        dy_sb = abs(sensor[1] - beacon[1])
        distance = dx_sb + dy_sb
        for y in range(sensor[1] - distance, sensor[1] + distance + 1):
        #for y in [where_y]:
            for x in range(sensor[0] - distance, sensor[0] + distance + 1):
                if (x, y) in [sensor, beacon]:
                    continue
                dx = abs(x - sensor[0])
                dy = abs(y - sensor[1])
                if (dx + dy) <= distance:
                    is_not_at.add((x, y))
    #print(len(is_not_at))
    if where_y == 10:
        print_map(data, is_not_at)
    return len([(x, y) for x, y in is_not_at if y == where_y])


def find_not_covered(ranges, xmin, xmax):
    not_covered = [(xmin, xmax)]
    for xmin, xmax in ranges:
        new_not_covered = []
        for xmin_nc, xmax_nc in not_covered:
            if xmin_nc < xmin <= xmax_nc and xmax >= xmax_nc:
                #      |    |
                #         ------
                # ->   | |
                new_not_covered.append((xmin_nc, xmin - 1))
            elif xmin_nc < xmin < xmax_nc and xmin_nc < xmax < xmax_nc:
                #   |     |
                #     ---
                # ->||   ||
                new_not_covered += [(xmin_nc, xmin - 1), (xmax + 1, xmax_nc)]
            elif xmin <= xmin_nc and xmin_nc <= xmax < xmax_nc:
                #       |     |
                #     ----
                # ->      |   |
                new_not_covered.append((xmax + 1, xmax_nc))
            elif xmin <= xmin_nc <= xmax and xmin <= xmax_nc <= xmax:
                #  |   |
                # -------
                # -> this range is now completely covered
                continue
            else:
                # i think now we are not overlapping and don't give additional info
                # so we need to add the range again
                new_not_covered.append((xmin_nc, xmax_nc))
        not_covered = new_not_covered
    return not_covered




# PART 2
@measure_time
def solve2(data, ymax=4000000):
    for y in tqdm(range(0, ymax)):
        ranges = []
        for sensor, beacon in data:
            dx_sb = abs(sensor[0] - beacon[0])
            dy_sb = abs(sensor[1] - beacon[1])
            distance = dx_sb + dy_sb
            dx_max = distance - abs(y - sensor[1])
            if dx_max > 0:
                ranges.append((sensor[0] - dx_max, sensor[0] + dx_max))
        not_covered = find_not_covered(ranges, 0, ymax)
        if y == 1:
            print(ranges)
        if not_covered:
            print(not_covered)
            return not_covered[0][0] * 4000000 + y


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    #print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))


data = parse(open(Path(__file__).parent / "input.txt").read())
