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


class Grid:
    def __init__(self, data):
        self._rows = list(r for r in data.split("\n") if r != '')
        self.height = len(self._rows)
        self.width = len(self._rows[0])
        #print(self._rows, self.height, self.width)

    def __str__(self):
        return "\n".join(self._rows)

    def __getitem__(self, x):
        return Column(x, self._rows)

    def _start(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == "S":
                    return [(x, y, d) for d in Direction]

    def path_len(self):
        # find a valid path from start and return length
        for start_x, start_y, d in self._start():
            x, y, d = self._next_coord(start_x, start_y, d)
            steps = 1
            while (x, y) != (start_x, start_y):
                if n := self.next_direction(x, y, d):
                    print(f"{steps=} {x,y=}, from={d} to={n}")
                    steps += 1
                    x, y, d = self._next_coord(x, y, n)
                else:
                    print(f"STOP {steps=} {x,y=}, from={d} to={n}")
                    steps = 0
                    break
            if steps:
                return steps // 2

    def _next_coord(self, x, y, direction):
        #print(f"next_coord {x,y=} {direction}")
        match direction:
            case Direction.NORTH:
                return x, y - 1, direction
            case Direction.EAST:
                return x + 1, y, direction
            case Direction.SOUTH:
                return x, y + 1, direction
            case Direction.WEST:
                return x - 1, y, direction

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

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read())
        return grid.path_len()

if __name__ == "__main__":
    print("- "*30)
    print(main("example"))
    print(main("example2"))
    print(main("example3"))
    print(main("input"))
