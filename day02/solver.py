import sys
from collections import deque

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [line for line in raw_data.strip().split("\n")]


SCORINGS = {
    "A X": 3,
    "A Y": 6,
    "A Z": 0,
    "B X": 0,
    "B Y": 3,
    "B Z": 6,
    "C X": 6,
    "C Y": 0,
    "C Z": 3,
}


def score_line(line):
    shape = line.split()[1]
    score = SCORINGS[line]
    if shape == "X":
        score += 1
    elif shape == "Y":
        score += 2
    elif shape == "Z":
        score += 3
    return score


# PART 1
@measure_time
def solve1(data):
    score = 0
    for line in data:
        score += score_line(line)
    return score


# PART 2
@measure_time
def solve2(data):
    score = 0
    scorings = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    for line in data:
        goal = line.split()[1]
        theirs = line.split()[0]
        if theirs == "A":
            winning = "Y"
            loosing = "Z"
            draw = "X"
        elif theirs == "B":
            winning = "Z"
            loosing = "X"
            draw = "Y"
        elif theirs == "C":
            winning = "X"
            loosing = "Y"
            draw = "Z"
        if goal == "X":
            score += 0
            score += scorings[loosing]
        elif goal == "Y":
            score += 3
            score += scorings[draw]
        elif goal == "Z":
            score += 6
            score += scorings[winning]
    return score


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

