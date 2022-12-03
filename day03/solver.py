import sys

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().split("\n"):
        n = len(line) // 2
        out.append((line[:n], line[n:]))
    return out


def get_priority(s):
    if s.isupper():
        return s.encode()[0] - 38
    return s.encode()[0] - 96


# PART 1
@measure_time
def solve1(data):
    total = 0
    for r1, r2 in data:
        for c in r1:
            if c in r2:
                total += get_priority(c)
                break
    return total


def find_common(rucksacks):
    for c in rucksacks[0]:
        for r in rucksacks[1:]:
            if not c in r:
                break
        else:
            return c


# PART 2
@measure_time
def solve2(data):
    total = 0
    for start, stop in zip(range(0, len(data), 3), range(3, len(data) + 1, 3)):
        group = data[start:stop]
        rucksacks = [r1 + r2 for r1, r2 in group]
        total += get_priority(find_common(rucksacks))
    return total


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
