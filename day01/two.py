STRINGS = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        0: "zero"}

STRINGS_REV={k: v[::-1] for k, v in STRINGS.items()}

def find_num(line, strings):
    for i in range(len(line)):
        if line[i] in "0123456789":
            return int(line[i])
        for n, s in strings.items():
            if line[i:].startswith(s):
                return n


def calibration_values(line):
    return (10 * find_num(line, STRINGS)) + find_num(line[::-1], STRINGS_REV)


def calibration_sum(filename):
    with open(filename) as fileh:
        return sum(calibration_values(line) for line in fileh)


if __name__ == "__main__":
    print(calibration_sum("example2"))
    print(calibration_sum("input"))
