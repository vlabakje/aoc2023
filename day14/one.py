import itertools

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

    def tilt(self):
        rocks = list(self.rocks())
        for x, y in rocks:
            self.move(x, y, 0)

    def move(self, x, y, direction):
        y_ = y
        while y_ != 0:
            if self[x][y_-1] == ".":
                y_ -= 1
            else:
                break
        if y_ != y:
            self[x][y] = "."
            self[x][y_] = "O"

    def load(self):
        for y in range(self.height):
            yield (self.height-y) * self._rows[y].count("O")

    def rocks(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == "O":
                    yield x, y


def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read().strip())
        grid.tilt()
        return sum(grid.load())


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
