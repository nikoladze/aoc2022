#!/usr/bin/env python

import sys
from pathlib import Path
from collections import defaultdict

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


class Shell:
    def __init__(self):
        self.dir = "/"

    def cd(self, dir):
        if dir == "/":
            self.dir = "/"
        elif dir == "..":
            self.dir = "/".join(self.dir[:-1].split("/")[:-1]) + "/"
        else:
            self.dir = self.dir + dir + "/"


def print_fstree(fstree, start="/", indent=""):
    for child in fstree[start]:
        if isinstance(child, tuple):
            size, filename = child
            print(f"{indent}- {filename} (file, size={size})")
        else:
            print(f"{indent}- {child} (dir)")
            print_fstree(fstree, start=start + child + "/", indent=indent + "  ")


def sum_directories(fstree):
    dirsizes = defaultdict(int)

    def sum_dir(dir):
        for child in fstree[dir]:
            if isinstance(child, tuple):
                size, filename = child
                dirsizes[dir] += size
            else:
                subdir = dir + child + "/"
                sum_dir(subdir)
                dirsizes[dir] += dirsizes[subdir]

    sum_dir("/")

    return dirsizes


def get_fstree(data):
    shell = Shell()
    fstree = defaultdict(list)
    for line in data:
        if line.startswith("$ cd"):
            shell.cd(line.split()[-1])
            continue
        if line.startswith("$ ls"):
            continue
        if line.startswith("dir"):
            fstree[shell.dir].append(line.split()[1])
            continue
        size, filename = line.split()
        fstree[shell.dir].append((int(size), filename))
    return fstree


# PART 1
@measure_time
def solve1(data):
    fstree = get_fstree(data)
    dirsizes = sum_directories(fstree)
    return sum(v for v in dirsizes.values() if v <= 100000)


# PART 2
@measure_time
def solve2(data):
    fstree = get_fstree(data)
    dirsizes = sum_directories(fstree)
    total = dirsizes["/"]
    free = 70000000 - total
    to_free = 30000000 - free
    return min(v for v in dirsizes.values() if v >= to_free)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
