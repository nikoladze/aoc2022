#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [tuple(map(int, line.split(","))) for line in raw_data.strip().splitlines()]


def surroundings(x, y, z):
    for dx, dy, dz in [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    ]:
        yield x + dx, y + dy, z + dz


def surface(cubes, check_also=None):
    for pos in cubes:
        for pos2 in surroundings(*pos):
            if pos2 in cubes:
                continue
            if check_also is not None and pos2 in check_also:
                continue
            yield pos2


# PART 1
@measure_time
def solve1(data):
    cubes = set(data)
    total = 0
    return sum(1 for _ in surface(cubes))


# PART 2
@measure_time
def solve2(data):
    cubes = set(data)
    xs, ys, zs = [[x[i] for x in data] for i in range(3)]
    rx, ry, rz = [(min(x), max(x)) for x in [xs, ys, zs]]

    def outside_grid(x, y, z):
        for xi, ri in zip([x, y, z], [rx, ry, rz]):
            if xi < ri[0] or xi > ri[1]:
                return True
        return False

    surface_candidates = []
    clusters = {}
    in_cluster = {}
    ic = 0
    for pos in surface(cubes):
        surface_candidates.append(pos)
        in_cluster[pos] = ic
        clusters[ic] = {"contains": [pos], "outside": False, "done": False}
        ic += 1

    while not all(cluster["done"] for cluster in clusters.values()):
        ic, cluster = next(
            (i, cluster) for i, cluster in clusters.items() if not cluster["done"]
        )
        no_more_surface = True
        for pos in surface(set(cluster["contains"]), check_also=cubes):
            no_more_surface = False
            if outside_grid(*pos):
                cluster["outside"] = True
                cluster["done"] = True
                break
            if pos in in_cluster:
                ic_other = in_cluster[pos]
                other_cluster = clusters[ic_other]
                if other_cluster["done"]:
                    # add ourselves
                    other_cluster["contains"] += cluster["contains"]
                    for p in cluster["contains"]:
                        in_cluster[p] = ic_other
                    del clusters[ic]
                else:
                    # eat it up
                    cluster["contains"] += other_cluster["contains"]
                    for p in other_cluster["contains"]:
                        in_cluster[p] = ic
                    del clusters[ic_other]
                break
            cluster["contains"].append(pos)
        if no_more_surface:
            # this should now be one that's inside
            cluster["done"] = True

    total = 0
    for pos in surface_candidates:
        if clusters[in_cluster[pos]]["outside"]:
            total += 1
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
