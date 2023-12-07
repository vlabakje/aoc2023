from dataclasses import dataclass, field
from collections import Counter
from enum import IntEnum

class Types(IntEnum):
    FIVE = 1
    FOUR = 2
    FULLHOUSE = 3
    THREE = 4
    TWOPAIR = 5
    ONEPAIR = 6
    HIGH = 7
    NONE = 8

CARDVALUES={v: k for k,v in enumerate("AKQJT98765432J")}

@dataclass(order=True)
class Hand:
    cards: str = field(compare=False)
    bid: int = field(compare=False)
    order: tuple = field(init=False, repr=False)

    def __post_init__(self):
        self.order = tuple([self._type()] + [CARDVALUES[c] for c in self.cards])

    def _type(self):
        c = Counter(self.cards)
        if c["J"] == 5:  # catch the edge case of "JJJJJ"
            c = Counter("22222")
        elif c["J"] > 0:
            c.update(c.most_common(1)[0][0] * c.pop("J"))
        match tuple(sorted(c.values())):
            case (_, ):
                return Types.FIVE
            case (1, 4):
                return Types.FOUR
            case (2, 3):
                return Types.FULLHOUSE
            case (1, 1, 3):
                return Types.THREE
            case (1, 2, 2):
                return Types.TWOPAIR
            case (1, 1, 1, 2):
                return Types.ONEPAIR
            case (1, 1, 1, 1, 1):
                return Types.HIGH
            case _:
                raise NotImplementedError(f"invalid hand {self.cards=} {c=}")

def main(filename):
    with open(filename) as fileh:
        hands = sorted([Hand(p[0], int(p[1])) for p in map(lambda line: line.split(), fileh)], reverse=True)
        return sum(rank * hand.bid for rank, hand in enumerate(hands, start=1))

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
