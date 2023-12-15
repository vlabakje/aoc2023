def main(filename):
    with open(filename) as fileh:
        hm = {i:[] for i in range(256)}
        for data in fileh.read().strip().split(","):
            update(hm, data)
        return sum(scores(hm))


def update(hm, data):
    def find(hl, label):
        for i, box in enumerate(hm[hl]):
            if box[0] == label:
                return i
    hl, label, op, fl = parse(data)
    #print(f"{label=} {hash_algo(label)=} {op=} {fl=})")
    match op:
        case "-":
            if (ix := find(hl, label)) != None:
                del hm[hl][ix]
        case "=":
            if (ix := find(hl, label)) != None:
                hm[hl][ix] = (label, fl)
            else:
                hm[hl].append((label, fl))
        case _:
            raise NotImplementedError(op)

def parse(data):
    fl = None
    if data[-1].isdigit():
        fl, data = int(data[-1]), data[:-1]
    label, op = data[:-1], data[-1]
    return hash_algo(label), label, op, fl


def scores(hm):
    for hl, box in hm.items():
        for i, b in enumerate(box, start=1):
            yield (hl+1) * i * b[1]


def hash_algo(data):
    h = 0
    for c in data:
        h = (h + ord(c)) * 17 % 256
    return h


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
