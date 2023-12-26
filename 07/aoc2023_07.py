
card_key = {s: n for n, s in enumerate('23456789TJQKA', 2)}

def load_game(fname):
    hands = []
    bids = []
    with open(fname) as istream:
        for line in istream:
            hand, bid = line.strip().split(' ')
            hands.append(tuple(card_key[s] for s in hand))
            bids.append(int(bid))
    return hands, bids

def analyze(hand, *, jokers=False):
    if jokers:
        numjokers = hand.count(11)
        h = tuple(c for c in hand if c != 11)
        hand = tuple(0 if c == 11 else c for c in hand)
    else:
        numjokers = 0
        h = hand
    counts = sorted((h.count(c) for c in set(h)), reverse=True)
    if not counts:
        counts = [numjokers]
    else:
        counts[0] += numjokers
    return tuple(counts), hand

def winnings(game, *, jokers=False):
    hands, bids = game
    values = [analyze(h, jokers=jokers) for h in hands]
    sortidcs = sorted(range(len(hands)), key=values.__getitem__)
    return sum(n * bids[idx] for n, idx in enumerate(sortidcs, 1))

if __name__ == '__main__':
    testgame = load_game('testinput')
    game = load_game('input')

    assert winnings(testgame) == 6440
    print(winnings(game))

    assert winnings(testgame, jokers=True) == 5905
    print(winnings(game, jokers=True))
