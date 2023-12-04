
import numpy as np

def load_cards(fname):
    cards = []
    with open(fname) as istream:
        for line in istream:
            cardnum, content = line.strip().split(': ')
            cards.append(tuple(np.fromstring(s, dtype=int, sep=' ')
                               for s in content.split(' | ')))
    return cards

def numwinners(card):
    return np.intersect1d(*card).size

def value(card):
    numwins = numwinners(card)
    if not numwins:
        return 0
    return np.power(2, numwins - 1)

def valuesum(cards):
    return sum(value(card) for card in cards)

def process(cards):
    copies = np.ones(len(cards), dtype=int)
    for i, card in enumerate(cards):
        copies[i + 1:i + 1 + numwinners(card)] += copies[i]
    return copies.sum()

if __name__ == '__main__':
    testcards = load_cards('testinput')
    cards = load_cards('input')

    assert valuesum(testcards) == 13
    print(valuesum(cards))

    assert process(testcards) == 30
    print(process(cards))
