def reflection_detect(lines):
    #print(f"reflection_detect {lines[0]=} {len(lines)=}")
    for i in range(0, len(lines)-1):
        if sum(difference(lines[i-j], lines[i+1+j]) for j in range(min(i+1, len(lines)-i-1))) == 1:
            return i+1

def difference(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)

def columnar(data):
    out = []
    for c in range(len(data[0])):
        out.append("".join(data[r][c] for r in range(len(data))))
    return out

def reflection_number(data):
    number = 0
    if row := reflection_detect(list(data.split("\n"))):
        #print(f"{row=}")
        number += 100 * row
    elif col := reflection_detect(columnar(list(data.split("\n")))):
        #print(f"{col=}")
        number += col
    assert number != 0, "\n" + "\n".join(columnar(list(data.split("\n"))))
    return number

def main(filename):
    with open(filename) as fileh:
        return sum(reflection_number(data.strip()) for data in fileh.read().split("\n\n"))


if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
