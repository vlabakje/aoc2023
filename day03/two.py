class Column:
    def __init__(self, x, grid):
        self.x = x
        self.grid = grid
    
    def __getitem__(self, y):
        return self.grid.lines[y][self.x]

class Grid:
    def __init__(self, source):
        self.source = source
        self.lines = [l for l in self.source.split("\n") if len(l)]
        assert all(len(l) == len(self.lines[0]) for l in self.lines)
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        self._columns = [Column(x, self) for x in range(self.height)]
        self.numbers = list(self._numbers())

    def stars(self):
        for y in range(self.height):
            for x in range(self.width):
                if self[x][y] == "*":
                    yield x, y

    def star_numberpair(self):
        for star_x, star_y in self.stars():
            # print(f"start {(star_x, star_y)=}")
            numbers = set()
            for x_ in (-1, 0, 1):
                for y_ in (-1, 0, 1):
                    if self[star_x+x_][star_y+y_].isdigit():
                        numbers.add(self.getnumber(star_x+x_, star_y+y_))
                        # print(f"{(star_x+x_, star_y+y_)=} {numbers=}")
            if len(numbers) == 2:
                numberlist = list(numbers)
                yield int(numberlist[0][2]) * int(numberlist[1][2])
            # print(f"end {(star_x, star_y)=} {numbers=}")
            
            
    def getnumber(self, x, y):
        # print(f"getnumber {x=} {y=}")
        for nx, ny, nn in self.numbers:
            if y == ny and x in range(nx, nx+len(nn)+1):
                # print(f"getnumber out {nx=} {ny=} {nn=}")
                return nx, ny, nn

    def _numbers(self):
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

    def __getitem__(self, x):
        return self._columns[x]

def main(filename):
    with open(filename) as fileh:
        grid = Grid(fileh.read())
        return sum(grid.star_numberpair())

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
