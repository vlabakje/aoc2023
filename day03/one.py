class Grid:
    def __init__(self, source):
        self.source = source
        self.lines = [l for l in self.source.split("\n") if len(l)]
        assert all(len(l) == len(self.lines[0]) for l in self.lines)
        self.height = len(self.lines)
        self.width = len(self.lines[0])

    def numbers(self):
        # loop though the grid and yield (x, y, str(number)) tuples
        for y in range(self.height):
            current = ""
            for x in range(self.width):
                # print(x, y, current, self[x][y], self[x][y].isdigit())
                if self[x][y].isdigit():
                    current += self[x][y]
                elif current:
                    yield (x-len(current), y, current)
                    current = ""
            if current:
                yield (x-len(current)+1, y, current)

    def around(self, x, y, xlen):
        def valid(a, b):
            return 0 <= a < self.width and 0 <= b < self.height
        for y_ in (y-1, y+1):
            for x_ in range(x-1, x+xlen+1):
                if valid(x_, y_):
                    yield x_, y_
        if valid(x-1, y):
            yield x-1, y
        if valid(x+xlen, y):
            yield x+xlen, y

    def is_part(self, x, y, number):
        for x_, y_ in self.around(x, y, len(number)):
            # print(f"{x_=} {y_=} {self[x_][y_]=}")
            if self[x_][y_] not in ".0123456789":
                return True
        return False
    
    def part_numbers(self):
        for x, y, number in self.numbers():
            # print(x, y, number, self.is_part(x, y, number))
            if self.is_part(x, y, number):
                yield int(number)

    def __getitem__(self, x):
        class Column:
            def __init__(self, x, grid):
                self.x = x
                self.grid = grid
            
            def __getitem__(self, y):
                return self.grid.lines[y][x]
        return Column(x, self)

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read())
        return sum(pn for pn in grid.part_numbers())

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
