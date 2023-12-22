import collections
import dataclasses

def main(filename):
    with open(filename) as fileh:
        restless = set(readbricks(fileh.read().strip()))
        z_total, rested, drops = rest_all(restless)
        total_drops = 0
        for brick in rested:
            _, _, drops = rest_all(rested.difference(set((brick,))))
            total_drops += drops
        return total_drops


def readbricks(data):
    for i, line in enumerate(data.split("\n"), start=97):
        a, _, b = line.partition("~")
        yield Brick(chr(i), Coords(*map(int, a.split(","))), Coords(*map(int, b.split(","))))
        
def rest_all(bricks):
    rested = set()
    z_total = 0
    drop_num = 0
    heightmap = collections.defaultdict(int)
    for brick in sorted(bricks, key=lambda b: min(b.a.z, b.b.z)):
        # given this heightmap, how far will brick drop?
        zt = min(c.z-heightmap[(c.x, c.y)]-1 for c in brick.coords())
        z_total += zt
        if zt:
            drop_num += 1
            brick = brick.movedown(zt)
        rested.add(brick)
        for c in brick.coords():
            heightmap[(c.x, c.y)] = c.z
    return z_total, rested, drop_num

@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int
    z: int

@dataclasses.dataclass(frozen=True)
class Brick:
    name: str
    a: Coords
    b: Coords

    def coords(self):
        # iterator for all coords of this brick
        for x in range(min(self.a.x, self.b.x), max(self.a.x, self.b.x)+1):
            for y in range(min(self.a.y, self.b.y), max(self.a.y, self.b.y)+1):
                for z in range(min(self.a.z, self.b.z), max(self.a.z, self.b.z)+1):
                    yield Coords(x, y, z)

    def movedown(self, n=1):
        return Brick(self.name, dataclasses.replace(self.a, z=self.a.z-n), dataclasses.replace(self.b, z=self.b.z-n))

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
