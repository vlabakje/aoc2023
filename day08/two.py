from math import gcd

def main(filename):
    with open(filename) as fileh:
        instr, mapdata = fileh.read().split("\n\n")
        # print(len(instr), instr)
        entries = {}
        for md in mapdata.split("\n"):
            current, _, lr = md.partition(" = ")
            l, _, r = lr[1:-1].partition(", ")
            entries[current] = (l, r)
        firstZ, secondZ, thirdZ = first_second_third(instr, entries)
        distances = {}
        for stream, step1 in firstZ.items():
            assert secondZ[stream] - step1 == thirdZ[stream] - secondZ[stream]
            # secondZ[stream] - step1 is the distance between repeats of secondZ
            distances[stream] = secondZ[stream] - step1
        return lowest_common_multiplier([distances[i] for i in sorted(distances.keys())])


def lowest_common_multiplier(numbers):
    out = 1
    for number in numbers:
        out = (number * out) // gcd(number, out)
    return out 


def first_second_third(instr, entries):
    firstZ, secondZ, thirdZ = {}, {}, {}
    steps = 0
    currents = [k for k in entries.keys() if k.endswith("A")]
    while not all(c.endswith("Z") for c in currents):
        newc = []
        direction = instr[steps%len(instr)]
        for i, current in enumerate(currents):
            newc.append(entries[current][direction=="R"])
            if newc[-1].endswith("Z"):
                if i not in firstZ:
                    firstZ[i] = steps
                elif i not in secondZ:
                    secondZ[i] = steps
                elif i not in thirdZ:
                    thirdZ[i] = steps
                if len(thirdZ) == len(currents):
                    return firstZ, secondZ, thirdZ
        currents = newc
        steps += 1

if __name__ == "__main__":
    print(main("input"))
