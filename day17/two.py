import collections
import dataclasses
import enum
import heapq

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
        self._cols = [Column(i, self._rows) for i in range(self.width)]

    def __str__(self):
        return "\n".join("".join(r) for r in self._rows)

    def debug(self, path):
        #print("\n".join(str(s) for s in path))
        c = {(s.x, s.y): s for s in path}
        d = {Directions.NORTH: "^", Directions.EAST: ">", Directions.SOUTH: "v", Directions.WEST: "<"}
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) in c:
                    line += d[c[(x, y)].d]
                else:
                    line += self[x][y]
            print(line)

    def __getitem__(self, x):
        return self._cols[x]

    def shortest(self):
        def path(node):
            p = []
            while node not in (s1, s2):
                p.append(node)
                node = previous_nodes[node]
            return list(reversed(p))
        previous_nodes = {}
        shortest_path = collections.defaultdict(lambda: 2**32)
        unvisited_nodes = []
        s1, s2 = Step(0, 0, Directions.EAST, 1), Step(0, 0, Directions.SOUTH, 1)
        shortest_path[s1] = 0
        shortest_path[s2] = 0
        heapq.heappush(unvisited_nodes, (0, s1))
        heapq.heappush(unvisited_nodes, (0, s2))
        while unvisited_nodes:
            #step = unvisited_nodes.popleft()
            dist, step = heapq.heappop(unvisited_nodes)
            #print(step, shortest_path[step], len(unvisited_nodes))
            for n_step in self.neighbours(step):
                if n_step in previous_nodes:
                    continue
                p = dist + int(self[n_step.x][n_step.y])
                if p < shortest_path[n_step]:
                    shortest_path[n_step] = p
                    previous_nodes[n_step] = step
                    heapq.heappush(unvisited_nodes, (p, n_step))
        shortest = None, 2**32
        for step, distance in shortest_path.items():
            if (step.x, step.y) == (self.width-1, self.height-1) and step.l > 3:
                if distance < shortest[1]:
                    shortest = step, distance
        return shortest[1], path(shortest[0])


    def neighbours(self, step):
        def valid(step):
            if 0 <= step.x < self.width and 0 <= step.y < self.height:
                yield step
        if step.l < 10:
            dx, dy = DELTAS[step.d]
            yield from valid(Step(step.x+dx, step.y+dy, step.d, step.l+1))
        if step.l < 4:
            return
        match step.d:
            case Directions.SOUTH | Directions.NORTH:
                yield from valid(Step(step.x-1, step.y, Directions.WEST, 1))
                yield from valid(Step(step.x+1, step.y, Directions.EAST, 1))
            case Directions.EAST | Directions.WEST:
                yield from valid(Step(step.x, step.y-1, Directions.NORTH, 1))
                yield from valid(Step(step.x, step.y+1, Directions.SOUTH, 1))

@dataclasses.dataclass(frozen=True, order=True)
class Step:
    x: int
    y: int
    d: Directions
    l: int


def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read().strip())
        l, p = grid.shortest()
        #grid.debug(p)
        return l


if __name__ == "__main__":
    #print(main("example2"))
    #print(main("example"))
    print(main("input"))
