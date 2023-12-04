def total_points(filename):
    with open(filename) as fileh:
        return sum(game_points(line) for line in fileh)


def game_points(line):
    card, _, numbers = line.partition(": ")
    draw, _, mine = numbers.partition(" | ")
    draw = set(map(int, draw.split()))
    mine = set(map(int, mine.split()))
    winning = draw & mine
    return 0 if not winning else 1 << len(winning)-1

if __name__ == "__main__":
    print(total_points("example"))
    print(total_points("input"))
