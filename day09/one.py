class Oasis:
    def __init__(self, report):
        self._report = report
        self._seq = [list(map(int, report.split()))]

    def __str__(self):
        l = len(str(max(abs(x) for x in self._seq[0]))) + 1
        return "\n".join(" "*(i*l//2) + 
            " ".join(f"{v:>{l}}" for v in line) + "\n" 
                for i, line in enumerate(self._seq))

    def analyze(self):
        assert len(self._seq) == 1
        while not all(x == 0 for x in self._seq[-1]):
            # append new line with differences from above
            self._seq.append(list())
            for i in range(len(self._seq[-2]) - 1):
                self._seq[-1].append(self._seq[-2][i+1] - self._seq[-2][i])

    def nextvalues(self):
        # reverse through the layers
        last = 0
        for i in range(len(self._seq)-1, -1, -1):
            n, last = last, self._seq[i][-1] + last
            yield last

def history(line):
    oasis = Oasis(line)
    oasis.analyze()
    *_, last = oasis.nextvalues()
    return last

def main(filename):
    with open(filename) as fileh:
        return sum(history(line) for line in fileh)


if __name__ == "__main__":
    print("*"*20)
    print(main("example"))
    print(main("input"))
