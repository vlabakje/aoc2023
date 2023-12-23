import collections

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
        return self._rows[0].index("."), 0

    def nodes_edges(self):
        def next_node(x, y, path):
            viable = [p for p in self.paths_from(x, y) if p not in path]
            if len(viable) == 1:
                return next_node(*viable[0], path + [(x, y)])
            if len(viable) > 1 or (x, y) == end or (x, y) == self.start():
                return x, y, len(path)
        end = self._rows[-1].index("."), self.height-1
        nodes = collections.defaultdict(dict)
        for x, y, exits in self.crossroads():
            for ex, ey in exits:
                if n := next_node(ex, ey, [(x, y)]):
                    nx, ny, plen = n
                    nodes[(nx, ny)][(x, y)] = plen
                    nodes[(x, y)][(nx, ny)] = plen  # path back
        return nodes

    def paths(self):
        nodes = self.nodes_edges()
        end = self._rows[-1].index("."), self.height-1
        def path_from(node, distance, seen):
            if node == end:
                yield distance
                return
            for possible, plen in nodes[node].items():
                if possible not in seen:
                    yield from path_from(possible, distance+plen, seen + [possible])
        for p in path_from(self.start(), 0, [self.start()]):
            yield p

    def paths_from(self, x, y):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x+dx < self.width and 0 <= y+dy < self.height:
                if self[x+dx][y+dy] != "#":
                    yield x+dx, y+dy

    def crossroads(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == "#":
                    continue
                exits = []
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x+dx < self.width and 0 <= y+dy < self.height:
                        if self[x+dx][y+dy] != "#":
                            exits.append((x+dx, y+dy))
                if len(exits) > 2:
                    yield x, y, exits

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read().strip())
        return max(grid.paths())

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
