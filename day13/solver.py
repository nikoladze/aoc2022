#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [[eval(expr) for expr in block.split("\n")] for block in raw_data.split("\n\n")]


def compare(left, right, indent=""):
    if isinstance(left, int) and isinstance(right, int):
        print(indent, f"- Compare {left} vs {right}")
        if left < right:
            print(indent, "  - Left side is smaller, so inputs are in the right order")
            return True
        if left > right:
            print(indent, "  - Right side is smaller, so inputs are not in the right order")
            return False
        return None
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    print(indent, f"- Compare {left} vs {right}")
    for left_element, right_element in zip(left, right):
        result = compare(left_element, right_element, indent=indent + "  ")
        if result is None:
            continue
        return result
    if len(left) < len(right):
        print(indent, "  - Left side ran out of items, so inputs are in the right order")
        return True
    if len(left) > len(right):
        print(indent, "  - Right side ran out of items, so inputs are not in the right order")
        return False


# PART 1
@measure_time
def solve1(data):
    return sum(i for i, right_order in enumerate([compare(left, right) for left, right in data], 1) if right_order)


# PART 2
@measure_time
def solve2(data):
    pass


#if __name__ == "__main__":
data = parse(open(Path(__file__).parent / "input.txt").read())
print("Part 1: {}".format(solve1(data)))
print("Part 2: {}".format(solve2(data)))

print("\nTime taken:")
for func, time in measure_time.times:
    print(f"{func:8}{time}s")
print("----------------")
print("total   {}s".format(sum(t for _, t in measure_time.times)))
