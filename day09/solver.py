#!/usr/bin/env python

import sys
from pathlib import Path

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.splitlines():
        ins, n = line.split()
        out.append((ins, int(n)))
    return out


def sign(x):
    return -1 if x < 0 else 1


def moved(pos, ins):
    dx, dy = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }[ins]
    return pos[0] + dx, pos[1] + dy


def followed(head_pos, tail_pos):
    dx, dy = (head_pos[0] - tail_pos[0], head_pos[1] - tail_pos[1])
    if abs(dx) > 1 and dy == 0:
        ux, uy = (1 * sign(dx), 0)
    elif dx == 0 and abs(dy) > 1:
        ux, uy = (0, 1 * sign(dy))
    elif (abs(dx) >= 1 and abs(dy) > 1) or (abs(dx) > 1 and abs(dy) >= 1):
        ux, uy = (1 * sign(dx), 1 * sign(dy))
    elif abs(dx) < 2 and abs(dy) < 2:
        # still touching
        ux, uy = (0, 0)
    else:
        raise ValueError("Invalid position!")
    return (tail_pos[0] + ux, tail_pos[1] + uy)


# PART 1
@measure_time
def solve1(data):
    visited = set()
    tail_pos = (0, 0)
    head_pos = (0, 0)
    for ins, n in data:
        for _ in range(n):
            head_pos = moved(head_pos, ins)
            tail_pos = followed(head_pos, tail_pos)
            visited.add(tail_pos)
    return len(visited)


def format_grid(head_pos, tail_positions):

    all_positions = [head_pos] + tail_positions
    min_x = min(pos[0] for pos in all_positions)
    min_y = min(pos[1] for pos in all_positions)
    max_x = max(pos[0] for pos in all_positions)
    max_y = max(pos[1] for pos in all_positions)

    nrows = 14
    ncols = 14

    grid = [
        [" " if (i + min_x + j + min_y) % 4 else "-" for i in range(ncols)]
        for j in range(nrows)
    ]

    def to_ij(x, y):
        return x - min_x + 2, -(y - min_y + 2)

    for n, pos in list(enumerate(tail_positions, 1))[::-1]:
        i, j = to_ij(*pos)
        grid[j][i] = str(n)

    i, j = to_ij(*head_pos)
    grid[j][i] = "H"

    return "\n".join("".join(row) for row in grid)


def generate_moves(data):
    head_position = (0, 0)
    tail_positions = [(0, 0) for _ in range(9)]
    for ins, n in data:
        for _ in range(n):
            head_position = moved(head_position, ins)
            lead_position = head_position
            for i in range(len(tail_positions)):
                follow_position = tail_positions[i]
                tail_positions[i] = followed(lead_position, follow_position)
                lead_position = tail_positions[i]
                yield head_position, tail_positions


# PART 2
@measure_time
def solve2(data):
    visited = set()
    for head_position, tail_positions in generate_moves(data):
        visited.add(tail_positions[-1])
    return len(visited)


def test_input():
    data = parse(open(Path(__file__).parent / "input.txt").read())
    assert solve1(data) == 5619
    assert solve2(data) == 2376


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
