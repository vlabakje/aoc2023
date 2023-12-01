def calibration_values(line):
    nums = [c for c in line if c in "0123456789"]
    return int(nums[0] + nums[-1])


def calibration_sum(filename):
    with open(filename) as fileh:
        return sum(calibration_values(line) for line in fileh)


if __name__ == "__main__":
    print(calibration_sum("example"))
    print(calibration_sum("input"))

