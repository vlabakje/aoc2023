import collections
import copy
import dataclasses
import math
from typing import Optional

def main(filename):
    with open(filename) as fileh:
        workflows, parts = workflows_parts(fileh.read().strip())
        ranges = {"in": {"x": {1: 4000}, "m": {1: 4000}, "a": {1: 4000}, "s": {1: 4000}}}
        total = 0
        q = collections.deque([ranges])
        while q:
            ranges = q.popleft()
            #print(f"{ranges=} {total=}")
            for workflow in ranges.keys():
                for wf_new, r_new in workflows[workflow].apply(ranges[workflow]):
                    if wf_new == "A":
                        m = 1
                        for d in r_new.values():
                            m *= math.prod(v-k+1 for k, v in d.items())
                        total += m
                    elif wf_new != "R":
                        q.append({wf_new: r_new})
        return total


def workflows_parts(data):
    wf_data, p_data = data.split("\n\n")
    workflows = dict()
    for line in wf_data.split("\n"):
        name, _, wf_parts = line[:-1].partition("{")
        workflows[name] = Workflow(name, [Condition(c) for c in wf_parts.split(",")])
    return workflows, None


@dataclasses.dataclass
class Condition:
    target: str
    field: Optional[str] = None
    op: Optional[str] = None
    n: Optional[int] = None

    def __init__(self, data):
        if ":" not in data:
            self.target = data
        else:
            t, _, target = data.partition(":")
            self.target = target
            if "<" in t:
                self.field, self.op, self.n = t.partition("<")
                self.n = int(self.n)
            elif ">" in t:
                self.field, self.op, self.n = t.partition(">")
                self.n = int(self.n)
            else:
                raise NotImplementedError("oh no!")


@dataclasses.dataclass
class Workflow:
    name: str
    conditions: [Condition]

    def apply(self, ranges):
        out1 = copy.deepcopy(ranges)
        for condition in self.conditions:
            if condition.field is None:
                yield condition.target, out1
            else:
                if condition.op == "<":
                    before, after = split_ranges(out1[condition.field], condition.n)
                    out2 = copy.deepcopy(out1)
                    out2[condition.field] = before
                    yield condition.target, out2
                    if len(after) == 0:
                        break
                    out1[condition.field] = after
                else:
                    before, after = split_ranges(out1[condition.field], condition.n+1)
                    out2 = copy.deepcopy(out1)
                    out2[condition.field] = after
                    yield condition.target, out2
                    if len(before) == 0:
                        break
                    out1[condition.field] = before


def split_ranges(ranges, split):
    #print(f"[split_ranges] {ranges=} {split=}")
    before, after = {}, {}
    for s, e in ranges.items():
        if s < split and e < split:
            before[s] = e
        elif s > split and e > split:
            after[s] = e
        else:
            before[s] = split-1
            after[split] = e
    return before, after


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
