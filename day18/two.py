def main(filename):
    with open(filename) as fileh:
        coords, line, area = coords_line_area(fileh.read().strip())
        return area // 2 + line // 2 + 1

DELTAS = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}


def coords_line_area(data, old=False):
    coords, line, area = [], 0, 0
    x, y = 0, 0
    for instr in data.split("\n"):
        d, n, rgb = instr.strip().split(" ")
        d = "RDLU"[int(rgb[-2])]
        n = int(rgb[2:-2], 16)
        # print(instr, d, n)
        if old:
            d, n, rgb = instr.strip().split(" ")
            n = int(n)
        dx, dy = DELTAS[d]
        nx, ny = x + (dx*n), y + (dy*n)
        coords.append((nx, ny, d))
        line += n
        area += x * ny - y * nx
        x, y = nx, ny
    return coords, line, area


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
