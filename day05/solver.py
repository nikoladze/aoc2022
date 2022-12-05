#!/usr/bin/env python

import sys
from pathlib import Path
import copy

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    raw_stack, raw_instructions = raw_data.split("\n\n")
    raw_stack = raw_stack.splitlines()
    n_stacks = int(raw_stack[-1].strip()[-1])
    stacks = [[] for _ in range(n_stacks)]
    for line in raw_stack[-2::-1]:
        for i, j in enumerate(range(1, 4 * n_stacks, 4)):
            try:
                item = line[j]
            except IndexError:
                item = " "
            if item != " ":
                stacks[i].append(item)
    n_from_to = []
    for line in raw_instructions.splitlines():
        _, n, _, f, _, t = line.split()
        n, f, t = (int(i) for i in (n, f, t))
        f = f - 1
        t = t - 1
        n_from_to.append((n, f, t))
    return stacks, n_from_to


# PART 1
@measure_time
def solve1(data):
    stacks, n_from_to = data
    stacks = copy.deepcopy(stacks)
    for n, f, t in n_from_to:
        for _ in range(n):
            item = stacks[f].pop()
            stacks[t].append(item)
    return "".join(stack[-1] for stack in stacks)


# PART 2
@measure_time
def solve2(data):
    stacks, n_from_to = data
    stacks = copy.deepcopy(stacks)
    for n, f, t in n_from_to:
        move_stack = []
        for _ in range(n):
            item = stacks[f].pop()
            move_stack.insert(0, item)
        stacks[t].extend(move_stack)
    return "".join(stack[-1] for stack in stacks)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
