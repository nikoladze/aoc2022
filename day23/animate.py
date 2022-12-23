#!/usr/bin/env python3

import pickle
from itertools import chain
import PIL.Image
from tqdm.auto import tqdm
import numpy as np

with open("trace.pkl", "rb") as f:
    trace = pickle.load(f)

xs = set(chain(*[[x for x, y in s] for s in trace]))
ys = set(chain(*[[y for x, y in s] for s in trace]))
xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)

img = np.zeros((ymax - ymin + 1, xmax - xmin + 1), dtype=np.uint8)

for ii, positions in tqdm(enumerate(trace)):
    img[:] = 0
    for j, y in enumerate(range(ymin, ymax + 1)):
        for i, x in enumerate(range(xmin, xmax + 1)):
            if (x, y) in positions:
                img[j, i] = 255
    PIL.Image.fromarray(img).save(f"frames/{ii:03d}.png")
