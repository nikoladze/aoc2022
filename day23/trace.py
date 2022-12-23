#!/usr/bin/env python3

from solver import solve, parse
import pickle

with open("input.txt") as f:
    data = parse(f.read())

trace = []
solve(data, trace=trace)

with open("trace.pkl", "wb") as f:
    pickle.dump(trace, f)
