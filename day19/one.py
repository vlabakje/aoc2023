import dataclasses
from typing import Optional

def main(filename):
    with open(filename) as fileh:
        workflows, parts = workflows_parts(fileh.read().strip())
        total = 0
        for part in parts:
            workflow = "in"
            while workflow not in "RA":
                print(workflow)
                workflow = workflows[workflow].apply(part)
            if workflow == "A":
                total += sum(part.values())
        return total


def workflows_parts(data):
    wf_data, p_data = data.split("\n\n")
    workflows = dict()
    for line in wf_data.split("\n"):
        name, _, wf_parts = line[:-1].partition("{")
        workflows[name] = Workflow(name, [Condition(c) for c in wf_parts.split(",")])
    parts = []
    for line in p_data.split("\n"):
        p = {}
        for l in line[1:-1].split(","):
            k, _, v = l.partition("=")
            p[k] = int(v)
        parts.append(p)
    return workflows, parts


@dataclasses.dataclass
class Condition:
    field: Optional[str]
    op: Optional[callable]
    target: str

    def __init__(self, data):
        if ":" not in data:
            self.target = data
            self.field = None
            self.op = None
        else:
            t, _, target = data.partition(":")
            self.target = target
            if "<" in t:
                self.field, _, v = t.partition("<")
                self.op = lambda x: x < int(v)
            elif ">" in t:
                self.field, _, v = t.partition(">")
                self.op = lambda x: x > int(v)
            else:
                raise NotImplementedError("oh no!")

    def applies(self, part):
        #print("applies", self, part)
        if self.field:
            if self.field in part:
                return self.op(part[self.field])
        return True


@dataclasses.dataclass
class Workflow:
    name: str
    conditions: [Condition]

    def apply(self, part):
        for condition in self.conditions:
            if condition.applies(part):
                return condition.target

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
