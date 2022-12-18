#!/usr/bin/env python

import sys
from pathlib import Path
from collections import defaultdict

import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.splitlines():
        valve, destinations = line.strip().split("; ")
        words = valve.split()
        valve = words[1]
        rate = int(words[4].split("=")[1])
        destinations = " ".join(destinations.split()[4:])
        destinations = tuple(destinations.split(", "))
        out.append(((valve, rate), destinations))
    return out


# PART 1
@measure_time
def solve1(data):
    destinations = {}
    rates = {}
    for (valve, rate), valve_destinations in data:
        destinations[valve] = valve_destinations
        rates[valve] = rate

    for valve, valve_destinations in list(destinations.items()):
        destinations[valve] = sorted(
            valve_destinations, key=lambda x: rates[x], reverse=True
        )

    total_minutes = 30
    state_scores = defaultdict(list)
    all_scores = set()

    def search(pos="AA", open_valves=frozenset(), score=0, time=0):

        for prev_score, prev_time in state_scores[(pos, open_valves)]:
            if prev_score >= score and prev_time <= time:
                # we've been here *and* it took same or less time
                # *and* we had a same or better score
                return score
        all_scores.add(score)
        state_scores[(pos, open_valves)].append((score, time))

        if time >= total_minutes:
            return score

        scores = []
        for action in [OPEN] + list(destinations[pos]):
            new_valves = open_valves
            dest = pos
            valve_score = 0
            if action == OPEN:
                if pos in open_valves:
                    continue
                if rates[pos] == 0:
                    continue
                new_valves = new_valves | {pos}
                valve_score += rates[pos] * (total_minutes - (time + 1))
            else:
                dest = action
            scores.append(search(dest, new_valves, score + valve_score, time + 1))

        return max(scores + [0])

    res = search()
    assert res == max((max(score for score, _ in l) for l in state_scores.values()))
    assert res == max(all_scores)
    return res


OPEN = 1

# PART 2
@measure_time
def solve2(data):
    destinations = {}
    rates = {}
    for (valve, rate), valve_destinations in data:
        destinations[valve] = valve_destinations
        rates[valve] = rate

    for valve, valve_destinations in list(destinations.items()):
        destinations[valve] = sorted(
            valve_destinations, key=lambda x: rates[x], reverse=True
        )

    total_minutes = 26
    state_scores = {}



    def search(pos_me="AA", pos_elefant="AA", open_valves=frozenset(), score=0, time=0, ident=""):
        def iprint(*args, **kwargs):
            #print(ident, *args, **kwargs)
            pass
        #iprint(f"{pos_me=}, {pos_elefant=}, {open_valves=}, {score=}, {time=}")
        if time >= total_minutes:
            return score
        try:
            prev_score, prev_time = state_scores[(pos_me, pos_elefant, open_valves)]
            if prev_score >= score and prev_time <= time:
                # we've been here *and* it took same or less time
                # *and* we had a same or better score
                return score
        except KeyError:
            pass
        state_scores[(pos_me, pos_elefant, open_valves)] = (score, time)

        iprint()
        iprint(f"== Minute {time+1} ==")
        iprint(f"{open_valves=}")

        scores = []
        for my_action in [OPEN] + list(destinations[pos_me]):
            for elefant_action in [OPEN] + list(destinations[pos_elefant]):
                new_valves = open_valves
                dest_me = pos_me
                dest_elefant = pos_elefant
                valve_score = 0
                # elefant
                if elefant_action == OPEN:
                    if pos_elefant in open_valves:
                        continue
                    if rates[pos_elefant] == 0:
                        continue
                    new_valves = new_valves | {pos_elefant}
                    valve_score += rates[pos_elefant] * (total_minutes - (time + 1))
                else:
                    dest_elefant = elefant_action
                # me
                if my_action == OPEN:
                    if pos_me in open_valves:
                        continue
                    if rates[pos_me] == 0:
                        continue
                    if elefant_action == OPEN and pos_elefant == pos_me:
                        # if the elefant is in the [same] room *badumm ts*
                        # i'll let him open the valve (only one of us can do it)
                        continue
                    new_valves = new_valves | {pos_me}
                    valve_score += rates[pos_me] * (total_minutes - (time + 1))
                else:
                    dest_me = my_action

                iprint(f"{my_action=}, {elefant_action=}")
                scores.append(
                    search(
                        dest_me, dest_elefant, new_valves, score + valve_score, time + 1, ident=ident + " "
                    )
                )

        return max(scores + [0])

    res = search()
    print(len(state_scores))
    return res


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    #print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
