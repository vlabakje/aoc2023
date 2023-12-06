import multiprocessing as mp

class Mapper():
    def __init__(self, data):
        seed_data, *block_data = list(data.split("\n\n"))
        s = list(map(int, seed_data.split(": ")[1].split()))
        self.seeds = [(s[i], s[i+1]) for i in range(0, len(s), 2)]
        self.maps = {}
        for b in block_data:
            b = b.split("\n")
            source, _, dest = b[0].split(" ")[0].partition("-to-")
            self.maps[source] = Map(source, dest, b[1:])
        # print(self.seeds)

    def map(self, source, n):
        return self.maps[source].map(n)

    def final_locations_per_seed(self, n):
        source = "seed"
        # print(f"seed {n}")
        while source != "location":
            # print(f"{source=} {n=}")
            source, n = self.map(source, n)
        # print(f"result {n}")
        return n

    def min_for_range(self, q, start, length):
        q.put(min(self.final_locations_per_seed(i) for i in range(start, start+length+1)))

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
        q = mp.Queue()
        processes = []
        for start, length in mapper.seeds:
            processes.append(mp.Process(target=mapper.min_for_range, args=(q, start, length)))
            processes[-1].start()
        [p.join() for p in processes]
        results = []
        while not q.empty():
            results.append(q.get())
        return min(results)

if __name__ == "__main__":
    print("this will produce the correct result but you can brew a cup of coffee and watch it go stale while it does")
    print(main("example"))
    print(main("input"))
