from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

PIPES = {
        "|": (Direction.NORTH, Direction.SOUTH),
        "-": (Direction.EAST,  Direction.WEST),
        "L": (Direction.NORTH, Direction.EAST),
        "J": (Direction.NORTH, Direction.WEST),
        "7": (Direction.SOUTH, Direction.WEST),
        "F": (Direction.SOUTH, Direction.EAST)
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
        #print(self._rows, self.height, self.width)

    def __str__(self):
        return "\n".join("".join(r) for r in self._rows)

    def tostr(self, path, enclosed):
        out = ""
        for y, r in enumerate(self._rows):
            for x, c in enumerate(r):
                if (x, y) in enclosed:
                    out += "I"
                elif c == ".":
                    out += "O"
                elif (x, y) in path:
                    out += c
                else:
                    out += " "
            out += "\n"
        return out

    def __getitem__(self, x):
        return Column(x, self._rows)

    def _start(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == "S":
                    return [(x, y, d) for d in Direction]

    def path_len(self):
        # find a valid path from start and return length
        for start_x, start_y, start_d in self._start():
            x, y, d = self._next_coord(start_x, start_y, start_d)
            path = set([(start_x, start_y), (x, y)])
            steps = 1
            while (x, y) != (start_x, start_y):
                if n := self.next_direction(x, y, d):
                    steps += 1
                    x, y, d = self._next_coord(x, y, n)
                    path.add((x, y))
                else:
                    steps = 0
                    break
            if steps:
                return start_x, start_y, start_d, path, x, y, d

    def _next_coord(self, x, y, direction):
        #print(f"next_coord {x,y=} {direction}")
        match direction:
            case Direction.NORTH: return x, y - 1, direction
            case Direction.EAST:  return x + 1, y, direction
            case Direction.SOUTH: return x, y + 1, direction
            case Direction.WEST:  return x - 1, y, direction

    def next_direction(self, x, y, source):
        match source:
            case Direction.NORTH: source = Direction.SOUTH
            case Direction.SOUTH: source = Direction.NORTH
            case Direction.EAST: source = Direction.WEST
            case Direction.WEST: source = Direction.EAST
        cell = self[x][y]
        if cell not in PIPES or source not in PIPES[cell]:
            return None
        return PIPES[cell][0 if PIPES[cell][1] == source else 1]

    def pipe_start(self, start_x, start_y, start_d, x, y, d):
        assert start_x == x and start_y == y
        match d:
            case Direction.NORTH: d = Direction.SOUTH
            case Direction.SOUTH: d = Direction.NORTH
            case Direction.EAST: d = Direction.WEST
            case Direction.WEST: d = Direction.EAST
        for p, directions in PIPES.items():
            if directions == (start_d, d) or directions == (d, start_d):
                return p

    def enclosed_coords(self, path):
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in path:
                    self[x][y] = "."
        for y in range(self.height):
            valid = False
            for x in range(self.width):
                if self[x][y] in "|LJ":
                    valid = not valid
                elif self[x][y] == "." and valid:
                    yield (x, y)

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read())
        start_x, start_y, start_d, path, x, y, d = grid.path_len()
        grid[x][y] = grid.pipe_start(start_x, start_y, start_d, x, y, d)
        enclosed = list(grid.enclosed_coords(path))
        return len(enclosed)

if __name__ == "__main__":
    print(main("example"))
    print(main("example2"))
    print(main("example3"))
    print(main("example4"))
    print(main("example5"))
    print(main("input"))
