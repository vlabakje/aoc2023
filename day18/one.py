def main(filename):
    with open(filename) as fileh:
        coords = set(gen_coords(fileh.read().strip()))
        return len(coords) + flood_count(coords)

DELTAS = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}

def gen_coords(data):
    x, y = 0, 0
    for line in data.split("\n"):
        d, n, rgb = line.strip().split(" ")
        dx, dy = DELTAS[d]
        for _ in range(int(n)):
            yield x, y
            x, y = x + dx, y + dy
    yield x, y


def bounds(coords):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for c in coords:
        min_x, max_x = min(min_x, c[0]), max(max_x, c[0])
        min_y, max_y = min(min_y, c[1]), max(max_y, c[1])
    return min_x, max_x, min_y, max_y


def flood_count(coords):
    min_x, max_x, min_y, max_y = bounds(coords)
    y = min_y + 1
    for x in range(min_x, max_x+1):
        if (x, y) in coords:
            x += 1
            break
    q = [(x, y)]
    fill = set(q)
    while q:
        x, y = q.pop()
        for nx, ny in neighbors(x, y):
            if min_x <= nx <= max_x or min_y <= ny <= max_y:
                if (nx, ny) in coords or (nx, ny) in fill:
                    continue
                else:
                    fill.add((nx, ny))
                    q.append((nx, ny))
            else:
                raise NotImplementedError("out of bounds", nx, ny)
    return len(fill)


def neighbors(x, y):
    for xd in (-1, 0, 1):
        for yd in (-1, 0, 1):
            if (xd, yd) != (0, 0):
                yield x+xd, y+yd

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
