def main(filename):
    with open(filename) as fileh:
        times, _, distances = fileh.read().partition("\n")
        times = times.replace(" ", "")
        distances = distances.replace(" ", "")
        return sum(ways_to_beat(int(times.split(":")[1]), int(distances.split(":")[1])))


def ways_to_beat(time, distance):
    for t in range(time+1):
        if (time-t) * t > distance:
            yield 1


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
