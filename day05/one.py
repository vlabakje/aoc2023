class Mapper():
    def __init__(self, data):
        seed_data, *block_data = list(data.split("\n\n"))
        self.seeds = list(map(int, seed_data.split(": ")[1].split()))
        self.maps = {}
        for b in block_data:
            b = b.split("\n")
            source, _, dest = b[0].split(" ")[0].partition("-to-")
            self.maps[source] = Map(source, dest, b[1:])
        # print(self.seeds)

    def map(self, source, n):
        return self.maps[source].map(n)

    def final_locations_per_seed(self):
        for n in self.seeds:
            source = "seed"
            # print(f"seed {n}")
            while source != "location":
                # print(f"{source=} {n=}")
                source, n = self.map(source, n)
            # print(f"result {n}")
            yield n


class Map():
    def __init__(self, source, dest, data):
        self.source = source
        self.dest = dest
        self._ranges = []
        for d in data:
            if d:
                self._ranges.append(Range(*map(int, d.split())))

    def map(self, n):
        for r in self._ranges:
            # print(f"{self.source=} {self.dest=} {r.source=} {r.dest=} {r.length=}")
            if n in r:
                # print("match")
                return self.dest, r.map(n)
        return self.dest, n
            

class Range():
    def __init__(self, dest, source, length):
        self.dest = dest
        self.source = source
        self.length = length
    
    def __contains__(self, n):
        return self.source <= n < self.source+self.length

    def map(self, n):
        assert n in self
        offset = n - self.source
        return offset + self.dest

def main(filename):
    with open(filename) as fileh:
        mapper = Mapper(fileh.read())
        return min(mapper.final_locations_per_seed())

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
