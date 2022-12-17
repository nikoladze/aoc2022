#!/usr/bin/env python

import sys
from pathlib import Path
from itertools import cycle, count
from collections import deque

import utils


measure_time = utils.stopwatch()

ROCKS = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


@measure_time
def parse(raw_data):
    rocks = [lines.split("\n") for lines in ROCKS.strip().split("\n\n")]
    jet_pattern = raw_data.strip()
    return rocks, jet_pattern


WALL = (0, 8)
FLOOR = 0


def simulate(data, stop_after=None, find_repetiton_maxlen=None):
    rocks, jet_pattern = data
    rocks = cycle(rocks)
    jet_pattern = cycle(jet_pattern)
    grid = {}

    seen_increase_sequences = {}

    def can_move(rock, pos):
        for y, line in zip(count(pos[1], -1), rock):
            for x, s in zip(count(pos[0], 1), line):
                if s != "#":
                    # position not covered by this rock
                    continue
                if y == FLOOR:
                    return False
                if x in WALL:
                    return False
                try:
                    if grid[(x, y)] == "#":
                        # another block already here
                        return False
                except KeyError:
                    pass
        return True

    def draw(rock, pos):
        for y, line in zip(count(pos[1], -1), rock):
            for x, s in zip(count(pos[0], 1), line):
                if s != "#":
                    # only draw "#"
                    continue
                grid[x, y] = "#"

    n_stopped = 0
    tower_height = 0
    if find_repetiton_maxlen is not None:
        current_increase_sequence = deque(maxlen=find_repetiton_maxlen)
    while True:
        rock = next(rocks)
        # pos is upper left edge
        pos = (3, tower_height + 3 + len(rock))
        while True:
            move = next(jet_pattern)
            if move == ">":
                try_pos = (pos[0] + 1, pos[1])
            else:
                try_pos = (pos[0] - 1, pos[1])
            if can_move(rock, try_pos):
                pos = try_pos
            try_pos = (pos[0], pos[1] - 1)
            if can_move(rock, try_pos):
                pos = try_pos
            else:
                # stopped
                draw(rock, pos)
                n_stopped += 1
                new_tower_height = max(y for (x, y), v in grid.items() if v == "#")
                if find_repetiton_maxlen is not None:
                    increase = new_tower_height - tower_height
                    current_increase_sequence.append(increase)
                    key = tuple(current_increase_sequence)
                    if key in seen_increase_sequences:
                        last_tower_height, last_n_stopped = seen_increase_sequences[key]
                        return (
                            current_increase_sequence,
                            new_tower_height,
                            n_stopped,
                            last_n_stopped,
                        )
                    else:
                        seen_increase_sequences[key] = (new_tower_height, n_stopped)
                tower_height = new_tower_height
                break
        if stop_after is not None and n_stopped >= stop_after:
            return tower_height


# PART 1
@measure_time
def solve1(data):
    return simulate(data, stop_after=2022)


# PART 2
@measure_time
def solve2(data):
    # try to find repeating sequence (of height increases) of length 1000
    _, tower_height, n_stopped, last_n_stopped = simulate(
        data, find_repetiton_maxlen=100
    )
    # find the actual repeating sequence
    # (could be optimized since we now know where the sequence starts - whatever)
    actual_sequence_length = n_stopped - last_n_stopped
    increase_sequence, tower_height, n_stopped, _ = simulate(
        data, find_repetiton_maxlen=actual_sequence_length
    )
    # look how often the sequence is going to repeat
    # for the remainder, take partial sequence of height increases
    ntot = 1000000000000
    nleft = ntot - n_stopped
    n_sequences = nleft // len(increase_sequence)
    hregular = n_sequences * sum(increase_sequence)
    hremain = sum(list(increase_sequence)[: (nleft % len(increase_sequence))])
    return tower_height + hregular + hremain


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
