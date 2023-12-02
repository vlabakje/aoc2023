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


def possible(game, max_red, max_green, max_blue):
    header, _, rolls = game.partition(": ")
    n = game_n(header)
    for roll in rolls.split(";"):
        rgb = roll_to_rgb(roll)
        if max_red < rgb["red"] or max_green < rgb["green"] or max_blue < rgb["blue"]:
            return 0
    return n

def main(filename, max_red, max_green, max_blue):
    with open(filename) as fileh:
        return sum(possible(game, max_red, max_green, max_blue) for game in fileh)


if __name__ == "__main__":
    print(main("example", 12, 13, 14))
    print(main("input", 12, 13, 14))
