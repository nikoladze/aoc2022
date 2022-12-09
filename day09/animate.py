#!/usr/bin/env python3

from pathlib import Path
import sys
import time
from solver import generate_moves, format_grid, parse

with open(Path(__file__).parent / "input.txt") as f:
    data = parse(f.read())


for head_position, tail_positions in generate_moves(data):
    sys.stdout.write("\n")
    grid = format_grid(head_position, tail_positions)
    sys.stdout.write(grid)
    nlines = len(grid.split("\n"))
    sys.stdout.write(f"\033[{nlines}A")
    sys.stdout.flush()
    time.sleep(0.001)
