def main(filename):
    with open(filename) as fileh:
        instr, mapdata = fileh.read().split("\n\n")
        print(instr)
        entries = {}
        for md in mapdata.split("\n"):
            current, _, lr = md.partition(" = ")
            l, _, r = lr[1:-1].partition(", ")
            entries[current] = (l, r)
        print(entries)
        current = "AAA"
        steps = 0
        while current != "ZZZ":
            direction = instr[steps%len(instr)]
            if direction == "L":
                current = entries[current][0]
            else:
                current = entries[current][1]
            print(steps, direction, current)
            steps += 1
        return steps


if __name__ == "__main__":
    print("="*20)
    print(main("example"))
    print(main("example2"))
    print(main("input"))
