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


class MonkeyCalculator:
    def __init__(self, data):
        self.dag = {}
        self.initial_results = {}
        self.operation = {}
        for monkey, job in data:
            if len(job) > 1:
                self.dag[monkey] = [job[0], job[2]]
                self.operation[monkey] = {
                    "+": op.add,
                    "-": op.sub,
                    "*": op.mul,
                    "/": op.truediv,
                }[job[1]]
            else:
                self.initial_results[monkey] = int(job[0])

    def eval(self, start="root", results=None):
        if results is None:
            results = self.initial_results
        results = results.copy()

        def eval_monkey(monkey):
            try:
                return results[monkey]
            except KeyError:
                pass
            a, b = self.dag[monkey]
            return self.operation[monkey](eval_monkey(a), eval_monkey(b))

        return eval_monkey(start)

    def eval_diff(self, me=0):
        results = dict(self.initial_results, humn=me)
        root_monkeys = self.dag["root"]
        m1, m2 = root_monkeys
        return self.eval(m1, results) - self.eval(m2, results)


# PART 1
@measure_time
def solve1(data):
    calc = MonkeyCalculator(data)
    return int(calc.eval())


# PART 2
@measure_time
def solve2(data):
    calc = MonkeyCalculator(data)
    # Secant method
    # start with 0, 1
    x1, x2 = 0, 1
    y1, y2 = calc.eval_diff(x1), calc.eval_diff(x2)
    while True:
        # y1 = a * x1 + b
        # -> b = y - (a * x1)
        # 0 = a * x + b
        # -> x = -b / a
        a = (y2 - y1) / (x2 - x1)
        b = y1 - (a * x1)
        x_new = -b / a
        y_new = calc.eval_diff(x_new)
        if y_new == 0:
            return int(x_new)
        x1, x2 = x2, x_new
        y1, y2 = y2, y_new


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
