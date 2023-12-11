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
        for y in range(self.height)[::-1]:
            if "#" not in self._rows[y]:
                self._rows.insert(y, self._rows[y][:])
                self.height += 1
        for x in range(self.width)[::-1]:
            if "#" not in self[x]:
                for y in range(self.height):
                    self._rows[y].insert(x, ".")
                self.width += 1
    
    def galaxys(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == "#":
                    yield x, y

    def galaxypairs(self):
        yield from itertools.combinations(self.galaxys(), 2)


    def shortest_paths(self):
        for one, two in self.galaxypairs():
            yield abs(one[0] - two[0]) + abs(one[1] - two[1])

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read())
        grid.expand()
        #print(grid)
        return sum(grid.shortest_paths())


if __name__ == "__main__":
    print(" -=|=- "*12)
    print(main("example"))
    print(main("input"))
