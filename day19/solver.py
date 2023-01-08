#!/usr/bin/env python

import sys
from pathlib import Path
from itertools import chain
from functools import cache

import utils


measure_time = utils.stopwatch()

FrozenCounter = tuple[int, ...]
Blueprint = tuple[FrozenCounter, ...]


ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


@measure_time
def parse(raw_data: str) -> list[Blueprint]:
    out = []
    for line in raw_data.splitlines():
        line = line.split(": ")[1]
        blueprint = []
        for instruction in line.split(". "):
            instruction = instruction.replace(".", "")
            robot = instruction.split()[1]
            made_from = instruction.split("costs ")[1].split(" and ")
            made_from = [ins.split() for ins in made_from]
            counts = [0, 0, 0, 0]
            for n, q in made_from:
                i = {"ore": ORE, "clay": CLAY, "obsidian": OBSIDIAN, "geode": GEODE}[q]
                counts[i] = int(n)
            blueprint.append(tuple(counts))
        out.append(tuple(blueprint))
    return out


def can_make(blueprint: Blueprint, counts: FrozenCounter):
    yield list(counts), None  # not building anything is always an option
    for i_robot, made_from in enumerate(blueprint):
        new_counts = list(counts)
        for i_counts, n in enumerate(made_from):
            if new_counts[i_counts] < n:
                break
            new_counts[i_counts] -= n
        else:
            yield new_counts, i_robot


@cache
def max_n_geodes(n: int, minute: int, n_robots: int, max_minute: int) -> int:
    for m in range(minute, max_minute):
        n += n_robots
        n_robots += 1
    return n


@cache
def max_required(blueprint: Blueprint, i_robot: int) -> int:
    return max(
        chain(
            *(
                (
                    n
                    for i_resource, n in enumerate(requirements)
                    if i_resource == i_robot
                )
                for requirements in blueprint
            )
        )
    )


def already_enough_of(blueprint: Blueprint, i_robot: int, robots: list) -> bool:
    if i_robot == GEODE:
        return False
    if robots[i_robot] > max_required(blueprint, i_robot):
        return True
    return False


def search(blueprint: Blueprint, max_minute: int = 24) -> int:
    best_n_geodes = 0
    visited = set()

    minute = 0
    counts = (0, 0, 0, 0)
    robots = (1, 0, 0, 0)
    q = []
    q.append((minute, counts, robots))
    while q:
        minute, counts, robots = q.pop()

        if counts[GEODE] > best_n_geodes:
            best_n_geodes = counts[GEODE]
            print(f"new {best_n_geodes=}")

        if minute >= max_minute:
            continue

        key = (minute, counts, robots)
        if key in visited:
            continue
        visited.add(key)

        for new_counts, building in can_make(blueprint, counts):
            new_robots = list(robots)
            for k in range(len(new_counts)):
                new_counts[k] += new_robots[k]
            if building is not None:
                new_robots[building] += 1
                if already_enough_of(blueprint, building, new_robots):
                    continue
            if (
                max_n_geodes(
                    new_counts[GEODE],
                    minute + 1,
                    new_robots[GEODE],
                    max_minute,
                )
                <= best_n_geodes
            ):
                continue
            q.append(
                (
                    minute + 1,
                    tuple(new_counts),
                    tuple(new_robots),
                )
            )

    print(f"final {best_n_geodes=}")
    return best_n_geodes


# PART 1
@measure_time
def solve1(data):
    result = 0
    for i, blueprint in enumerate(data, 1):
        result += i * search(blueprint)
    return result


# PART 2
@measure_time
def solve2(data):
    result = 1
    for blueprint in data[:3]:
        result *= search(blueprint, max_minute=32)
    return result


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
