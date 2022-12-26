#!/usr/bin/env python

import sys
from pathlib import Path
from collections import defaultdict
import math

import utils


measure_time = utils.stopwatch()


def snafu_to_int(digits):
    digits = [int(d) if d not in "=-" else {"-": -1, "=": -2}[d] for d in digits]
    i = 0
    power = 0
    for d in reversed(digits):
        i += 5**power * d
        power += 1
    return i


def int_to_snafu(i):
    base5_digits = []
    max_p = int(math.log(i) / math.log(5))
    for power in range(max_p, -1, -1):
        n = i // 5**power
        base5_digits.append(n)
        i -= n * 5**power
    snaifu_digits = []

    def append(power, d, carry):
        d += carry
        if d > 2:
            nsub = (5 ** (power + 1) - (5**power) * d) // (5**power)
            snaifu_digits.append({0: "0", 1: "-", 2: "="}[nsub])
            carry = 1
        else:
            snaifu_digits.append(str(d))
            carry = 0
        return carry

    carry = 0
    for power, d in enumerate(reversed(base5_digits)):
        carry = append(power, d, carry)
    if carry != 0:
        carry = append(power + 1, 0, carry)
    assert carry == 0

    return "".join(snaifu_digits[::-1])


@measure_time
def parse(raw_data):
    return raw_data.splitlines()


# PART 1
@measure_time
def solve1(data):
    return int_to_snafu(sum(snafu_to_int(s) for s in data))


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
