def total_points(filename):
    cards = {card: [1, winning] for card, winning in card_winnings(filename)}
    for card in range(1, max(cards.keys())+1):
        for c in range(card+1, card+1+cards[card][1]):
            cards[c][0] += cards[card][0]
        # print(card, cards)
    return sum(card[0] for card in cards.values())

def card_winnings(filename):
    with open(filename) as fileh:
        for line in fileh:
            yield card_winning(line)

def card_winning(line):
    card, _, numbers = line.partition(": ")
    draw, _, mine = numbers.partition(" | ")
    draw = set(map(int, draw.split()))
    mine = set(map(int, mine.split()))
    winning = draw & mine
    return int(card.split()[1]), len(winning)

if __name__ == "__main__":
    print(total_points("example"))
    print(total_points("input"))
