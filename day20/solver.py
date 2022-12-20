#!/usr/bin/env python

import sys
from pathlib import Path

import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return list(map(int, raw_data.splitlines()))


def move_entry(l, i, steps):
    thing = l[i]
    l.pop(i)
    # note: l is now shorter since we popped!
    i_shift = steps % len(l)
    i_thing_after_me = i if i != len(l) else 0
    i_place_me_before = (i_thing_after_me + i_shift) % len(l)
    l.insert(
        i_place_me_before,
        thing,
    )


def score(l):
    for i, n in l:
        if n == 0:
            zero_tuple = (i, n)
            break
    zero_index = l.index(zero_tuple)
    return sum(l[(zero_index + k) % len(l)][1] for k in [1000, 2000, 3000])


def solve(data, key=1, n_iterations=1):
    orig = list(enumerate([i * key for i in data]))
    l = orig[:]
    for i in range(n_iterations):
        for i, steps in orig:
            elem = (i, steps)
            move_entry(l, l.index(elem), steps)
    return score(l)


# PART 1
@measure_time
def solve1(data):
    return solve(data)


# PART 2
@measure_time
def solve2(data):
    return solve(data, key=811589153, n_iterations=10)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
