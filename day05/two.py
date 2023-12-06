from dataclasses import dataclass

class Mapper():
    def __init__(self, data):
        seed_data, *block_data = list(data.split("\n\n"))
        self.seed = Series(list(map(int, seed_data.split(": ")[1].split())))
        print(self.seed)
        self.maps = {}
        for b in block_data:
            b = b.split("\n")
            source, _, dest = b[0].split(" ")[0].partition("-to-")
            self.maps[source] = Map(source, dest, b[1:])

    def final_locations_per_seed(self):
        source = "seed"
        while source != "location":
            source = self.maps[source].map(self.seed)
            #return
        yield self.seed.min()
        print(f"minimum {self.seed.min()=}")

class Map():
    def __init__(self, source, dest, data):
        self.source = source
        self.dest = dest
        self._ranges = []
        for d in data:
            if d:
                self._ranges.append(Range(*map(int, d.split())))

    def map(self, series):
        print(f"[mapping] s={self.source} d={self.dest} {series=}")
        for r in self._ranges:
            #print(f"mapping s={self.source} d={self.dest} rs={r.source} rd={r.dest} {r.length=} {series=}")
            if series.apply(r):
                break
        print(f"[mapping] done s={self.source} d={self.dest} {series=}")
        return self.dest
            

class Series():
    def __init__(self, seedpairs):
        self._series = {seedpairs[i]: seedpairs[i]+seedpairs[i+1]-1 for i in range(0, len(seedpairs), 2)}

    def apply(self, r):
        _series = {}
        changed = False
        for s, e in sorted(self._series.items()):
            if overlap := r.overlap(s, e):
                for a, b in r.remaining(s, e):
                    _series = add_series(_series, a, b)
                print(f"apply {overlap=} {r=} {_series=} {overlap[0]+r.offset()},{overlap[1]+r.offset()}")
                # assert overlap[0]+r.offset() not in _series
                #_series[overlap[0]+r.offset()] = overlap[1]+r.offset()
                _series = add_series(_series, overlap[0]+r.offset(), overlap[1]+r.offset())
                changed = True
            else:
                _series = add_series(_series, s, e)
        self._series = _series
        return changed

    def __repr__(self):
        return f"S({' '.join(str(k)+'-'+str(v) for k, v in sorted(self._series.items()))} "\
                f"{sum(v-k for k, v in self._series.items())})"

    def min(self):
        return min(self._series.keys())



def add_series(series, start, end):
    out ={}
    merged = False
    for s, e in series.items():
        o_s = max(start, s)
        o_e = min(end, e)
        if o_s <= o_e:
            out[min(start, s)] = max(end, e)
            merged = True
        else:
            out[s] = e
    if not merged:
        out[start] = end
    return out


@dataclass
class Range():
    dest: int
    source: int
    length: int
    
    def overlap(self, s, e):
        o_s = max(self.source, s)
        o_e = min(self.source + self.length, e)
        if o_s <= o_e:
            return o_s, o_e
    
    def remaining(self, s, e):
        out = []
        o = self.overlap(s, e)
        if s < o[0]:
            print(f"[remaining] {self=} {o=} {s=} {e=} {o[0]-1=}")
            out.append((s, o[0]-1))
        if e > o[1]:
            print(f"[remaining2] {self=} {o=} {s=} {e=} {o[0]=}")
            out.append((o[1], e))
        return out

    def offset(self):
        return self.dest - self.source

    def __repr__(self):
        return f"Range(s{self.source}-{self.source+self.length-1} d{self.dest}-{self.dest+self.length-1} o={self.dest-self.source})"


def main(filename):
    with open(filename) as fileh:
        mapper = Mapper(fileh.read())
        return min(mapper.final_locations_per_seed())

if __name__ == "__main__":
    print("="*20)
    print(main("example"))
    #r = main("input")
    print(r)
    assert r != 530455385
