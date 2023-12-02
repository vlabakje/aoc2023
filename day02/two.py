from functools import reduce

def game_n(header):
    g, _, n = header.partition(" ")
    assert g == "Game"
    return int(n)


def roll_to_rgb(roll):
    out = {"red": 0, "green": 0, "blue": 0}
    for r in roll.split(", "):
        n, _, color = r.strip().partition(" ")
        assert color in out, f"{r=} {color=}"
        out[color] = int(n)
    return out


def power(game):
    min_rgb = {"red": 0, "green": 0, "blue": 0}
    header, _, rolls = game.partition(": ")
    n = game_n(header)
    for roll in rolls.split(";"):
        for color, count in roll_to_rgb(roll).items():
            min_rgb[color] = max(min_rgb[color], count)
    # print(f"{n=}, {min_rgb.values()=}")
    return reduce(lambda a, b: a*b, min_rgb.values())


def main(filename):
    with open(filename) as fileh:
        return sum(power(game) for game in fileh)


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
