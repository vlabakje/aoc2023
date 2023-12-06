from dataclasses import dataclass

class Mapper():
    def __init__(self, data):
        seed_data, *block_data = list(data.split("\n\n"))
        self.series = Series(list(map(int, seed_data.split(": ")[1].split())))
        print(self.series)
        self.maps = {}
        for b in block_data:
            b = b.split("\n")
            source, _, dest = b[0].split(" ")[0].partition("-to-")
            self.maps[source] = Map(source, dest, b[1:])

    def final_locations_per_seed(self):
        source = "seed"
        while source != "location":
            print(f"[map] {source} {self.maps[source]}")
            source = self.maps[source].map(self.series)
            #if source == "light": return
        yield self.series.min()
        print(f"minimum {self.series.min()=}")

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
        _news = dict()
        source = dict(series._series.items())
        #for s, e in sorted(series._series.items()):
        while len(source):
            print(f"  {source=}")
            s, e = min(source.keys()), source.pop(min(source.keys()))
            #_news = {}
            found = False
            for r in sorted(self._ranges, key=lambda r: r.source):
                if overlap := r.overlap(s, e):
                    print(f"  apply {overlap=} {s=} {e=} {r=} {_news=} {overlap[0]+r.offset()},{overlap[1]+r.offset()}")
                    for a, b in r.remaining(s, e):
                        print(f"    remainder: {a=}, {b=}")
                        if b == e:
                            source[a] = b
                        else:
                            _news = add_series(_news, a, b)
                    # assert overlap[0]+r.offset() not in _series
                    #_series[overlap[0]+r.offset()] = overlap[1]+r.offset()
                    _news = add_series(_news, overlap[0]+r.offset(), overlap[1]+r.offset())
                    found = True
                    break
            if not found:
                _news = add_series(_news, s, e)
            #_s = _news
            #print(f"[mapping] series {s=},{e=} completed {_s=} {r=}")
        series._series = _news
        print(f"[mapping] done s={self.source} d={self.dest} {series=}")
        return self.dest
        # old function
        for r in self._ranges:
            #print(f"mapping s={self.source} d={self.dest} rs={r.source} rd={r.dest} {r.length=} {series=}")
            if series.apply(r):
                break
        print(f"[mapping] done s={self.source} d={self.dest} {series=}")
        return self.dest
            

    def __repr__(self):
        return f"Map({', '.join(str(r) for r in self._ranges)})"

@dataclass
class Range():
    dest: int
    source: int
    length: int
    
    def overlap(self, s, e):
        o_s = max(self.source, s)
        o_e = min(self.source + self.length-1, e)
        if o_s <= o_e:
            return o_s, o_e
    
    def remaining(self, s, e):
        out = []
        o = self.overlap(s, e)
        if s < o[0]:
            #print(f"[remaining] {self=} {o=} {s=} {e=} {o[0]-1=}")
            out.append((s, o[0]-1))
        if e > o[1]:
            #print(f"[remaining2] {self=} {o=} {s=} {e=} {o[0]=}")
            out.append((o[1]+1, e))
        return out

    def offset(self):
        return self.dest - self.source

    def __repr__(self):
        return f"Range(s{self.source}-{self.source+self.length-1} d{self.dest}-{self.dest+self.length-1} o={self.dest-self.source})"

class Series():
    def __init__(self, seedpairs):
        self._series = {seedpairs[i]: seedpairs[i]+seedpairs[i+1]-1 for i in range(0, len(seedpairs), 2)}

    def __repr__(self):
        return f"S({' '.join(str(k)+'-'+str(v) for k, v in sorted(self._series.items()))} "\
                f"{sum(v-k+1 for k, v in self._series.items())})"

    def min(self):
        return min(self._series.keys())


def add_series(series, start, end):
    print(f"    [add_series] {series=} {start=} {end=}")
    out ={}
    merged = False
    for s, e in series.items():
        o_s = max(start, s)
        o_e = min(end, e)
        if o_s <= o_e:
            out[min(start, s)] = max(end, e)
            merged = True
        elif end + 1 == s:
            out[start] = e
            merged = True
        elif e + 1 == start:
            out[s] = end
            merged = True
        else:
            out[s] = e
    if not merged:
        out[start] = end
    return out


def main(filename):
    with open(filename) as fileh:
        mapper = Mapper(fileh.read())
        return min(mapper.final_locations_per_seed())

if __name__ == "__main__":
    print("="*20)
    print(main("example"))
    r = main("input")
    print(r)
    assert r != 530455385
