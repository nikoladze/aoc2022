#!/usr/bin/env python

import sys
from pathlib import Path
import logging

import utils


measure_time = utils.stopwatch()

logger = logging.getLogger(__name__)


@measure_time
def parse(raw_data):
    out = []
    monkeys_data = raw_data.split("\n\n")
    for monkey_data in monkeys_data:
        values = [
            line.strip().split(":")[1].strip()
            for line in monkey_data.strip().splitlines()[1:]
        ]
        monkey = {
            "start": tuple(map(int, values[0].split(","))),
            "op": values[1].split("=")[1].strip(),
            "test_div": int(values[2].split()[-1]),
            "targets": (int(values[3].split()[-1]), int(values[4].split()[-1])),
        }
        out.append(monkey)
    return out


def get_operation(s):
    left, op, right = s.split()
    if op == "*":
        fn = lambda a, b: a * b
    elif op == "+":
        fn = lambda a, b: a + b
    get_operand = []
    for operand in [left, right]:
        if operand == "old":
            get_operand.append(lambda old: old)
        else:
            get_operand.append(lambda old: int(operand))
    left, right = get_operand
    return lambda old: fn(left(old), right(old))


class Monkey:
    def __init__(self, start, op, test_div, targets):
        self.items = list(start)
        self.op = get_operation(op)
        self.test_div = test_div
        self.targets = targets
        self.n_inspected = 0

    def throw(self):
        items_and_targets = []
        for item in self.items:
            logger.debug("Inspect with %d", item)
            item = self.op(item) // 3
            logger.debug("Updated to: %d", item)
            logger.debug("%d divisible by %d?", item, self.test_div)
            if (item % self.test_div) == 0:
                logger.debug("True!")
                logger.debug("Throw to %d", self.targets[0])
                items_and_targets.append((item, self.targets[0]))
            else:
                logger.debug("False!")
                logger.debug("Throw to %d", self.targets[1])
                items_and_targets.append((item, self.targets[1]))
        self.n_inspected += len(self.items)
        self.items = []
        return items_and_targets


class Game:
    def __init__(self, monkeys):
        self.monkeys = monkeys

    def round(self):
        for i, monkey in enumerate(self.monkeys):
            logger.debug("Monkey %d", i)
            for item, target in monkey.throw():
                self.monkeys[target].items.append(item)


# PART 1
@measure_time
def solve1(data):
    game = Game([Monkey(**monkey_data) for monkey_data in data])
    for round in range(20):
        game.round()
    top1, top2 = sorted(monkey.n_inspected for monkey in game.monkeys)[-2:]
    return top1 * top2


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

    monkey = Monkey(**data[0])
