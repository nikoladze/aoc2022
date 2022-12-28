#!/usr/bin/env python

import sys
from pathlib import Path
from collections import deque

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    grid, pw = raw_data.split("\n\n")
    grid = grid.splitlines()
    instructions = []
    start = 0
    pos = 0
    while pos < len(pw):
        if pw[pos] in "LR":
            if start != pos:
                instructions.append(int(pw[start:pos]))
            instructions.append(pw[pos])
            start = pos + 1
        pos += 1
    if start != pos:
        instructions.append(int(pw[start:pos]))
    return grid, instructions


def print_grid(grid, x, y):
    grid = [list(row) for row in grid]
    nrows = len(grid)
    ncols = max(len(row) for row in grid)
    grid[y][x] = "o"
    grid.insert(0, [str(i % 10) for i in range(ncols)])
    grid.insert(0, [str(i // 10) for i in range(ncols)])
    grid[0].insert(0, "  ")
    grid[1].insert(0, "  ")
    for i, row in enumerate(grid[2:]):
        row.insert(0, f"{i:02d}")
    return "\n".join(["".join(row) for row in grid])


# PART 1
@measure_time
def solve1(data):
    grid, instructions = data
    facings = deque([0, 1, 2, 3])
    facing = facings[0]
    for i, c in enumerate(grid[0]):
        if c == ".":
            x, y = (i, 0)
            break

    def in_grid(x, y):
        if x < 0 or y < 0:
            return False
        try:
            c = grid[y][x]
        except IndexError:
            return False
        if c == " ":
            return False
        return True

    def wrap(x, y, dx, dy):
        while True:
            x2, y2 = x - dx, y - dy
            if not in_grid(x2, y2):
                return x, y
            x, y = x2, y2

    for instruction in instructions:
        if instruction == "L":
            facings.rotate(1)
        elif instruction == "R":
            facings.rotate(-1)
        else:
            facing = facings[0]
            dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][facing]
            for i in range(instruction):
                x2, y2 = (x + dx, y + dy)
                if not in_grid(x2, y2):
                    x2, y2 = wrap(x2, y2, dx, dy)
                if grid[y2][x2] == "#":
                    break
                x, y = x2, y2

    row = y + 1
    col = x + 1
    return 1000 * row + 4 * col + facing


class Cube:
    def __init__(self, grid, areas, connections):
        self.areas = areas
        self.connections = {
            # address as e.g. connections[1]["L"]
            # instead of connections[1][0]
            k: dict(zip("LRTB", v))
            for k, v in connections.items()
        }

        self.grid = grid
        self.nrows = len(self.grid)
        self.ncols = max(len(row) for row in self.grid)
        self.n_per_face = max(self.nrows, self.ncols) // 4
        self.velocities = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

        y = 0
        for x, c in enumerate(self.grid[0]):
            if c == ".":
                break
        self.pos = (x, y)

    def your_face(self, x, y):
        return int(self.areas[y // self.n_per_face][x // self.n_per_face])

    def border_you_run_into(self, x, y, dx, dy):
        if dx < 0 and x % self.n_per_face == 0:
            return "L"
        if dx > 0 and x % self.n_per_face == self.n_per_face - 1:
            return "R"
        if dy < 0 and y % self.n_per_face == 0:
            return "T"
        if dy > 0 and y % self.n_per_face == self.n_per_face - 1:
            return "B"
        raise IndexError(
            f"We don't seem to be running into any border with "
            f"{x=}, {y=}, {dx=}, {dy=} don't we?"
        )

    def topleft_for_face(self, face):
        for j, row in enumerate(self.areas):
            for i, test_face in enumerate(row):
                if test_face == ".":
                    continue
                test_face = int(test_face)
                if test_face == face:
                    return i * self.n_per_face, j * self.n_per_face

    def wrapped(self, x, y, dx, dy):
        """
        x, y: coordinates before wrapping
        dx, dy: moving velocity before wrapping
        returns updated x, y, dx, dy
        """
        face = self.your_face(x, y)
        border = self.border_you_run_into(x, y, dx, dy)
        goto = self.connections[face][border]
        goto_face = int(goto[0])
        goto_border = goto[1]

        # relative coordinates from top left of the face
        n = self.n_per_face
        rx, ry = x % n, y % n

        # first transfer into coordinates as if i would hit the top
        nx = n - rx - 1
        ny = n - ry - 1
        rx, ry = {
            "L": (ny, 0),
            "R": (ry, 0),
            "T": (rx, 0),
            "B": (nx, 0),
        }[border]

        # then from top to goal
        nx = n - rx - 1
        ny = n - ry - 1
        rx, ry = {
            "L": (0, rx),
            "R": (n - 1, nx),
            "T": (nx, 0),
            "B": (rx, n - 1),
        }[goto_border]

        # now find topleft, add rx, ry
        # and determine new dx, dy
        x, y = self.topleft_for_face(goto_face)
        x, y = x + rx, y + ry
        dx, dy = {
            "T": (0, 1),
            "B": (0, -1),
            "L": (1, 0),
            "R": (-1, 0),
        }[goto_border]

        return x, y, dx, dy

    def __str__(self):
        return print_grid(self.grid, *self.pos)

    @property
    def velocity(self):
        return self.velocities[0]

    @velocity.setter
    def velocity(self, v):
        for i in range(len(self.velocities)):
            if v == self.velocity:
                break
            self.rotate()
        else:
            raise ValueError(f"Invalid velocity `{v}`")

    def rotate(self, direction="L"):
        if direction == "L":
            self.velocities.rotate(1)
        elif direction == "R":
            self.velocities.rotate(-1)
        else:
            raise KeyError(f"Invalid rotation instruction `{direction}`")

    def in_grid(self, x, y):
        if x < 0 or y < 0:
            return False
        try:
            c = self.grid[y][x]
        except IndexError:
            return False
        if c == " ":
            return False
        return True

    def move(self, instruction):
        if isinstance(instruction, str):
            self.rotate(instruction)
            return

        dx, dy = self.velocity
        x, y = self.pos
        for i in range(instruction):
            x2, y2, dx2, dy2 = (x + dx, y + dy, dx, dy)
            if not self.in_grid(x2, y2):
                x2, y2, dx2, dy2 = self.wrapped(x, y, dx, dy)
            if self.grid[y2][x2] == "#":
                break
            x, y, dx, dy = x2, y2, dx2, dy2
            self.velocity = (dx, dy)
        self.pos = (x, y)


# hardcoded for my input
AREAS = [
    ".12.",
    ".3..",
    "45..",
    "6...",
]

# e.g. "4L" for the first entry of 1 means
# the left edge of area 1 is connected to the left edge of area 4
CONNECTIONS = {
    #    L     R     T     B
    #    ..    ..    ..    ..
    1: ["4L", "2L", "6L", "3T"],
    2: ["1R", "5R", "6B", "3R"],
    3: ["4T", "2B", "1B", "5T"],
    4: ["1L", "5L", "3L", "6T"],
    5: ["4R", "2R", "3B", "6R"],
    6: ["1T", "5B", "4B", "2T"],
}

# PART 2
@measure_time
def solve2(data, areas=AREAS, connections=CONNECTIONS):
    grid, instructions = data
    cube = Cube(grid, areas=areas, connections=connections)
    for instruction in instructions:
        cube.move(instruction)
    x, y = cube.pos
    row = y + 1
    col = x + 1
    facing = [(1, 0), (0, 1), (-1, 0), (0, -1)].index(cube.velocity)
    return 1000 * row + 4 * col + facing


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
