import collections
import dataclasses
import enum

class Directions(enum.IntEnum):
    NORTH=0
    EAST=1
    SOUTH=2
    WEST=3

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

    def _shoot(self, beam):
        # beam entering x, y results in one or more other beams
        # print("_shoot", beam, self[beam.x][beam.y])
        match self[beam.x][beam.y]:
            case "\\" if beam.direction in (Directions.NORTH, Directions.SOUTH):
                yield beam.next((beam.direction-1)%4)
            case "\\" if beam.direction in (Directions.EAST, Directions.WEST):
                yield beam.next((beam.direction+1)%4)
            case "/" if beam.direction in (Directions.NORTH, Directions.SOUTH):
                yield beam.next((beam.direction+1)%4)
            case "/" if beam.direction in (Directions.EAST, Directions.WEST):
                yield beam.next((beam.direction-1)%4)
            case "-" if beam.direction in (Directions.NORTH, Directions.SOUTH):
                yield beam.next(Directions.EAST)
                yield beam.next(Directions.WEST)
            case "|" if beam.direction in (Directions.WEST, Directions.EAST):
                yield beam.next(Directions.NORTH)
                yield beam.next(Directions.SOUTH)
            case _:  # straight ahead
                yield beam.next(beam.direction)
    
    def simulate(self):
        start = Beam(0, 0, Directions.EAST) 
        energized, beams = set([(start.x, start.y)]), set([start])
        dq = collections.deque()
        dq.append(start)
        while dq:
            for beam in self._shoot(dq.popleft()):
                if beam in beams:
                    continue
                if 0 <= beam.x < self.width and 0 <= beam.y < self.height:
                    energized.add((beam.x, beam.y))
                    beams.add(beam)
                    dq.append(beam)
        # self.print_energized(energized)
        return len(energized)

    def print_energized(self, energized):
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += "#" if (x, y) in energized else self[x][y]
            print(line)

@dataclasses.dataclass(frozen=True)
class Beam:
    x: int
    y: int
    direction: Directions

    def next(self, direction):
        dx, dy = DELTAS[direction]
        return Beam(self.x+dx, self.y+dy, direction)

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read().strip())
        #print(grid)
        return grid.simulate()

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
