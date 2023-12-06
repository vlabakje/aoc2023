def main(filename):
    with open(filename) as fileh:
        times, _, distances = fileh.read().partition("\n")
        total = 1
        for t, d in zip(map(int, times.split(": ")[1].split()), map(int, distances.split(": ")[1].split())):
            total *= sum(ways_to_beat(t, d))
        return total


def ways_to_beat(time, distance):
    for t in range(time+1):
        d = (time-t) * t
        if d > distance:
            yield 1


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
