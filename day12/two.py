import functools

def main(filename):
    with open(filename) as fileh:
        return sum(arrangement_count(line) for line in fileh if line)


def arrangement_count(line):
    mask, _, groups = line.partition(" ")
    mask, groups = "?".join(mask for _ in range(MULTIPLIER)), ",".join(groups for _ in range(MULTIPLIER))
    groups = list(map(int, groups.strip().split(",")))
    #print(f"{mask=} {groups=}")
    return valid_arrangements(mask, groups)


def valid_arrangements(mask, groups):
    minneeded = [sum(groups[i:])+len(groups)-i-1 for i in range(len(groups))]
    print("valid_arrangements", len(mask), minneeded)
    @functools.cache
    def fits(offset, group):
        if "." in mask[offset:offset+groups[group]]:
            return False
        if offset+groups[group] == len(mask):
            return True # end of the line
        if mask[offset+groups[group]] == "#":
            return False
        return True
    @functools.cache
    def arrangements(offset, group):
        out = 0
        if group == len(groups):
            return 1 if mask[offset:].count("#") == 0 else 0
        else:
            for o in range(offset, len(mask)-minneeded[group]+1):
                if "#" in mask[offset:o]:
                    break
                # try to fit groups[group] here
                if fits(o, group):
                    out += arrangements(o+groups[group]+1, group+1)
        # print(f"arrangements {offset=} {group=} {out=}")
        return out
    return arrangements(0, 0)  # vroom vroom


def valid(mask, groups, offset):
    # can you make these groups in this mask?
    maskg = tuple(len(g) for g in mask.split(".") if len(g) > 0)
    return maskg == tuple(groups)

MULTIPLIER=5
if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
