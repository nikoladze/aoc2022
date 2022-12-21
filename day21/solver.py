#!/usr/bin/env python

import sys
from pathlib import Path
from ast import literal_eval
import operator as op

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.splitlines():
        monkey, job = line.split(": ")
        out.append((monkey, job.split()))
    return out


# PART 1
@measure_time
def solve1(data):
    dag = {}
    results = {}
    operation = {}
    for monkey, job in data:
        if len(job) > 1:
            dag[monkey] = [job[0], job[2]]
            operation[monkey] = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv}[job[1]]
        else:
            results[monkey] = int(job[0])

    def eval_monkey(monkey="root"):
        try:
            return results[monkey]
        except KeyError:
            pass
        a, b = dag[monkey]
        return operation[monkey](eval_monkey(a), eval_monkey(b))

    return eval_monkey()

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

