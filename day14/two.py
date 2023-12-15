from collections import defaultdict
import enum
import itertools

class Directions(enum.Enum):
    NORTH=0
    WEST=1
    SOUTH=2
    EAST=3

DELTAS={
        Directions.NORTH: (0, -1),
        Directions.SOUTH: (0, 1),
        Directions.EAST: (1, 0),
        Directions.WEST: (-1, 0)
    }

class Column:
    def __init__(self, x, rows):
        self._x = x
        self._rows = rows

    def __getitem__(self, y):
        return self._rows[y][self._x]

    def __setitem__(self, y, value):
        self._rows[y][self._x] = value


class Grid:
    def __init__(self, data):
        self._rows = list(list(r) for r in data.split("\n") if r != '')
        self.height = len(self._rows)
        self.width = len(self._rows[0])

    def __str__(self):
        return "\n".join("".join(r) for r in self._rows)

    def __getitem__(self, x):
        return Column(x, self._rows)


    def cycle(self):
        for d in Directions:
            self.tilt(d)

    def tilt(self, direction):
        rocks = list(self.rocks())
        if direction in (Directions.SOUTH, Directions.EAST):
            rocks.sort(reverse=True)
        for x, y in rocks:
            self.move(x, y, direction)

    def move(self, x, y, direction):
        x_, y_ = x, y
        xd, yd = DELTAS[direction]
        for _ in range(max(self.height, self.width)):
            if 0 <= (x_+xd) < self.width and 0 <= (y_+yd) < self.height:
                if self[x_+xd][y_+yd] == ".":
                    x_, y_ = x_+xd, y_+yd
                    continue
            break
        if (x_, y_) != (x, y):
            #print(f"moving {x, y} to {x_, y_}")
            self[x][y] = "."
            self[x_][y_] = "O"

    def load(self):
        for y in range(self.height):
            yield (self.height-y) * self._rows[y].count("O")

    def rocks(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == "O":
                    yield x, y

    def load_after_cycles(self, n):
        seen = defaultdict(list)
        for i in range(n):
            h = hash(str(self._rows))
            if h in seen and len(seen[h]) == 3:
                #print(f"looped {i=} {h=} {sum(self.load())} {len(seen)=}")
                break
            else:
                seen[h].append((i, sum(self.load())))
            self.cycle()
        loop_d = seen[h][-1][0] - seen[h][-2][0]
        loop_s = seen[h][0][0]
        answer = ((n-loop_s) % loop_d ) + loop_s
        for v in seen.values():
            if v[0][0] == answer:
                return v[0][1]


def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read().strip())
        return grid.load_after_cycles(1_000_000_000)


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
