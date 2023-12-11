import itertools

class Column:
    def __init__(self, x, rows):
        self._x = x
        self._rows = rows

    def __getitem__(self, y):
        return self._rows[y][self._x]


class Grid:
    def __init__(self, data):
        self._rows = list(list(r) for r in data.split("\n") if r != '')
        self.height = len(self._rows)
        self.width = len(self._rows[0])
        #print(self._rows, self.height, self.width)

    def __str__(self):
        return "\n".join("".join(r) for r in self._rows)

    def __getitem__(self, x):
        return Column(x, self._rows)

    def expand(self):
        self.bigrows = set(y for y in range(self.height) if "#" not in self._rows[y])
        self.bigcols = set(x for x in range(self.width) if "#" not in self[x])
    
    def galaxys(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == "#":
                    yield x, y

    def galaxypairs(self):
        yield from itertools.combinations(self.galaxys(), 2)

    def shortest_paths(self):
        for one, two in self.galaxypairs():
            path = 0
            for x in range(min(one[0], two[0]), max(one[0], two[0]) + 0):
                path += VERY_VERY_FAR if x in self.bigcols else 1
            for y in range(min(one[1], two[1]), max(one[1], two[1]) + 0):
                path += VERY_VERY_FAR if y in self.bigrows else 1
            yield path

VERY_VERY_FAR=1_000_000

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read())
        grid.expand()
        return sum(grid.shortest_paths())


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
