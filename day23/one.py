import collections
import dataclasses
import enum
import heapq
import sys

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
        self._cols = [Column(i, self._rows) for i in range(self.width)]

    def __str__(self):
        return "\n".join("".join(r) for r in self._rows)

    def __getitem__(self, x):
        return self._cols[x]

    def start(self):
        return 0, self._rows[0].index(".")

    def paths(self, path):
        end = self.height-1, self._rows[-1].index(".")
        here = path[-1]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= here[0]+dx < self.width and 0 <= here[1]+dy < self.height:
                if (here[0]+dx, here[1]+dy) == end:
                    yield path # + [(here[0]+dx, here[1]+dy)]
                    return
                if (here[0]+dx, here[1]+dy) in path:
                    continue
                match self[here[0]+dx][here[1]+dy]:
                    case ".":
                        yield from self.paths(path + [(here[0]+dx, here[1]+dy)])
                    case "v" if (dx, dy) == (0, 1):
                        yield from self.paths(path + [(here[0]+dx, here[1]+dy)])
                    case "^" if (dx, dy) == (0, -1):
                        yield from self.paths(path + [(here[0]+dx, here[1]+dy)])
                    case ">" if (dx, dy) == (1, 0):
                        yield from self.paths(path + [(here[0]+dx, here[1]+dy)])
                    case "<" if (dx, dy) == (-1, 0):
                        yield from self.paths(path + [(here[0]+dx, here[1]+dy)])
        

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read().strip())
        #print(grid)
        return max(len(p) for p in grid.paths([grid.start()]))

if __name__ == "__main__":
    sys.setrecursionlimit(9000)
    print(main("example"))
    print(main("input"))
