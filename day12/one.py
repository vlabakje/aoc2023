def main(filename):
    with open(filename) as fileh:
        return sum(arrangement_count(line) for line in fileh if line)


def arrangement_count(line):
    mask, _, groups = line.partition(" ")
    groups = list(map(int, groups.strip().split(",")))
    s = sum(1 for a in arrangements(mask, groups, 0) if valid(a, groups, 0))
    print(f"{mask=} {groups=} {s=}")
    return s


def arrangements(mask, groups, offset):
    if "?" not in mask:
        yield mask
    else:
        if mask[offset] == "?":
            for x in (".#"):
                yield from arrangements(replace(mask, offset, x), groups, offset+1)
        else:
            yield from arrangements(mask, groups, offset+1)


def replace(source, offset, c):
    return source[:offset] + c + source[offset+1:]


def valid(mask, groups, offset):
    # can you make these groups in this mask?
    maskg = tuple(len(g) for g in mask.split(".") if len(g) > 0)
    return maskg == tuple(groups)

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
