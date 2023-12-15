def main(filename):
    with open(filename) as fileh:
        total = 0
        for step in fileh.read().strip().split(","):
            # print(step, hash_algo(step))
            total += hash_algo(step)
        return total


def hash_algo(data):
    h = 0
    for c in data:
        h = (h + ord(c)) * 17 % 256
    return h


if __name__ == "__main__":
    # print(hash_algo("HASH"))
    print(main("example"))
    print(main("input"))
