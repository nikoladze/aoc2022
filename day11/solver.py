#!/usr/bin/env python

import sys
from pathlib import Path
from operator import mul, add

import utils


measure_time = utils.stopwatch()


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


def get_operation(expr):
    def operand(operand_str):
        if operand_str == "old":
            return lambda old: old
        else:
            const_value = int(operand_str)
            return lambda old: const_value

    left, operator, right = expr.split()
    left, right = [operand(o) for o in [left, right]]
    operator = mul if operator == "*" else add

    return lambda old: operator(left(old), right(old))


class Monkey:
    def __init__(self, start, op, test_div, targets, divide_3=True):
        self.start = start
        self.op = get_operation(op)
        self.test_div = test_div
        self.targets = targets
        self.divide_3 = divide_3

        self.n_inspected = 0
        self._divisors = None
        self.items = None

    @property
    def divisors(self):
        return self._divisors

    @divisors.setter
    def divisors(self, divisors):
        self._divisors = set(divisors)
        self.items = {k: list(self.start) for k in self.divisors}

    def throw(self):
        items_and_targets = []
        n_items = len(list(self.items.values())[0])
        for i in range(n_items):
            item = {}
            for divisor in self.divisors:
                item[divisor] = self.op(self.items[divisor][i])
                if self.divide_3:
                    item[divisor] = item[divisor] // 3
                else:
                    item[divisor] = item[divisor] % divisor
            if not self.divide_3:
                div_condition = item[self.test_div] == 0
            else:
                div_condition = (item[self.test_div] % self.test_div) == 0
            if div_condition:
                target = self.targets[0]
            else:
                target = self.targets[1]
            items_and_targets.append((item, target))
        self.n_inspected += n_items
        self.items = {k: [] for k in self.divisors}
        return items_and_targets

    def append(self, items):
        for k, v in self.items.items():
            v.append(items[k])


class Game:
    def __init__(self, monkeys):
        self.monkeys = monkeys
        divisors = [monkey.test_div for monkey in self.monkeys]
        for monkey in self.monkeys:
            monkey.divisors = divisors

    def round(self):
        for i, monkey in enumerate(self.monkeys):
            for item, target in monkey.throw():
                self.monkeys[target].append(item)


def solve(data, n_rounds, divide_3):
    game = Game([Monkey(**monkey_data, divide_3=divide_3) for monkey_data in data])
    for round in range(n_rounds):
        game.round()
    top1, top2 = sorted(monkey.n_inspected for monkey in game.monkeys)[-2:]
    return top1 * top2


# PART 1
@measure_time
def solve1(data):
    return solve(data, 20, divide_3=True)


# PART 2
@measure_time
def solve2(data):
    return solve(data, 10000, divide_3=False)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
