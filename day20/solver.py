#!/usr/bin/env python

import sys
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
debug = logger.debug

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return list(map(int, raw_data.splitlines()))


def move_entry(l, i, steps):
    thing = l[i]
    thing_after_me = l[(i + 1) % len(l)]
    debug(f"{thing_after_me=}")
    l.pop(i)
    # note: l is now shorter since we popped!
    i_thing_after_me = l.index(thing_after_me)
    debug(f"{i_thing_after_me=}")
    i_shift = steps % len(l)
    debug(f"{i_shift=}")
    i_place_me_before = (i_thing_after_me + i_shift) % len(l)
    debug(f"{i_place_me_before=}")
    l.insert(
        i_place_me_before,
        thing,
    )


# PART 1
@measure_time
def solve1(data):
    l = list(enumerate(data[:]))
    debug("")
    debug([x[1] for x in l])
    for i, n in l[:]:
        i_curr = l.index((i, n))
        move_entry(l, i_curr, n)
        debug([x[1] for x in l])
        #input()
    for i, n in l:
        if n == 0:
            zero_tuple = (i, n)
            break
    debug(zero_tuple)
    return (
        l[(l.index(zero_tuple) + 1000) % len(l)][1]
        + l[(l.index(zero_tuple) + 2000) % len(l)][1]
        + l[(l.index(zero_tuple) + 3000) % len(l)][1]
    )


# PART 2
@measure_time
def solve2(data):
    key = 811589153
    orig = [i * key for i in data]
    orig = list(enumerate(orig[:]))
    l = orig[:]
    debug("")
    debug([x[1] for x in l])
    for i in range(10):
        for i, n in orig:
            i_curr = l.index((i, n))
            move_entry(l, i_curr, n)
            debug([x[1] for x in l])
            #input()
    for i, n in l:
        if n == 0:
            zero_tuple = (i, n)
            break
    debug(zero_tuple)
    return (
        l[(l.index(zero_tuple) + 1000) % len(l)][1]
        + l[(l.index(zero_tuple) + 2000) % len(l)][1]
        + l[(l.index(zero_tuple) + 3000) % len(l)][1]
    )



if __name__ == "__main__":
    logging.basicConfig(format="%(message)s")
    #logger.setLevel(logging.DEBUG)
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

