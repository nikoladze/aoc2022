#!/usr/bin/env python3

from pathlib import Path
from solver import solve, parse, format_cave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

with open(Path(__file__).parent / "input.txt") as f:
    data = parse(f.read())

trace = []
solve(data, with_floor=True, trace=trace)

fig, ax = plt.subplots(figsize=(5, 20))
ax.set_axis_off()

cave_map = trace.pop(0)
ims = []
for pos in trace[:1000]:
    cave_map[pos] = "o"
    array = np.array([[ord(l) for l in row] for row in format_cave(cave_map)], dtype=np.uint8)
    ims.append([ax.imshow(array, animated=True)])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
ani.save("movie.gif")
