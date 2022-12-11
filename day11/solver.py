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
        self.start = start
        self._modulos = None
        self.items = None
        self.op = get_operation(op)
        self.test_div = test_div
        self.targets = targets
        self.n_inspected = 0


    @property
    def modulos(self):
        return self._modulos

    @modulos.setter
    def modulos(self, modulos):
        self._modulos = modulos
        self.items = {k: list(self.start) for k in self.modulos}


    def throw(self):
        items_and_targets = []
        n_items = len(list(self.items.values())[0])
        for i in range(n_items):
            logger.debug("  Inspect item number %d", i)
            item = {}
            for modulo in self.modulos:
                #item[modulo] = self.op(self.items[modulo][i]) // 3
                item[modulo] = self.op(self.items[modulo][i])
                logger.debug("    Updated to: %d", item[modulo])
                item[modulo] = item[modulo] % modulo
                logger.debug("    Update modulo %d: %d", modulo, item[modulo])
            logger.debug("    Divisible by %d", self.test_div)
            if item[self.test_div] == 0:
                logger.debug("    True!")
                logger.debug("    Throw to %d", self.targets[0])
                items_and_targets.append((item, self.targets[0]))
            else:
                logger.debug("    False!")
                logger.debug("    Throw to %d", self.targets[1])
                items_and_targets.append((item, self.targets[1]))
        self.n_inspected += n_items
        self.items = {k: [] for k in self.modulos}
        return items_and_targets


    def append(self, items):
        for k, v in self.items.items():
            v.append(items[k])


class Game:
    def __init__(self, monkeys):
        self.monkeys = monkeys
        modulos = [monkey.test_div for monkey in self.monkeys]
        for monkey in self.monkeys:
            monkey.modulos = modulos


    def round(self):
        for i, monkey in enumerate(self.monkeys):
            logger.debug("Monkey %d", i)
            for item, target in monkey.throw():
                self.monkeys[target].append(item)


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
    game = Game([Monkey(**monkey_data) for monkey_data in data])
    for round in range(10000):
        game.round()
    top1, top2 = sorted(monkey.n_inspected for monkey in game.monkeys)[-2:]
    return top1 * top2


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
    game = Game([Monkey(**monkey_data) for monkey_data in data])
