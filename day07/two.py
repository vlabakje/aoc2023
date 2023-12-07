from dataclasses import dataclass
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
    cards: str
    bid: int

    def __post_init__(self):
        ix = [self._type()] + [CARDVALUES[c] for c in self.cards]
        self.sort_index = tuple(ix)

    def _type(self):
        c = Counter(self.cards)
        if c["J"] > 0:
            j = c["J"]
            del c["J"]
            if j == 5:
                c.update("2"*j)
            else:
                c.update(c.most_common(1)[0][0]*j)
        s = tuple(sorted(c.values()))
        if len(s) == 1:
            return Types.FIVE
        if s == (1, 4):
            return Types.FOUR
        if s == (2, 3):
            return Types.FULLHOUSE
        if s == (1, 1, 3):
            return Types.THREE
        if s == (1, 2, 2):
            return Types.TWOPAIR
        if s == (1, 1, 1, 2):
            return Types.ONEPAIR
        if s == (1, 1, 1, 1, 1):
            return Types.HIGH
        return Types.NONE

def main(filename):
    with open(filename) as fileh:
        hands = []
        for line in fileh:
            cards, _, bid = line.partition(" ")
            hands.append(Hand(cards, int(bid)))
        hands = sorted(hands, key=lambda h: h.sort_index, reverse=True)
        #for rank, h in enumerate(hands, start=1):
        #    print(rank, h, h.sort_index)
        return sum(rank * h.bid for rank, h in enumerate(hands, start=1))

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
