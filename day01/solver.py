import sys

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [[int(i) for i in block.split("\n")] for block in raw_data.strip().split("\n\n")]


# PART 1
@measure_time
def solve1(data):
    return max(sum(block) for block in data)


# PART 2
@measure_time
def solve2(data):
    return sum(sorted(sum(block) for block in data)[-3:])


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

