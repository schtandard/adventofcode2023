
spellings = {
    s: str(n) for n, s in enumerate([
        'one', 'two', 'three',
        'four', 'five', 'six',
        'seven', 'eight', 'nine',
    ], 1)
}

def getnum(line, spelled=False):
    if spelled:
        digits = []
        while line:
            for word, d in spellings.items():
                if line.startswith(word) or line.startswith(d):
                    digits.append(d)
                    break
            line = line[1:]
    else:
        digits = [c for c in line if c in spellings.values()]
    num = int(digits[0] + digits[-1])
    return num

def numsum(fname, spelled=False):
    with open(fname) as istream:
        return sum(getnum(line, spelled) for line in istream)

if __name__ == '__main__':
    assert numsum('testinput') == 142
    print(numsum('input'))

    assert numsum('testinput2', True) == 281
    print(numsum('input', True))
