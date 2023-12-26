
import numpy as np

def load_schematic(fname):
    # Returns fieldmap, numbers where fieldmap has the index of the number,
    # -1 for empty or -2 for symbol at each position.
    fields = np.genfromtxt(fname, dtype=str, delimiter=1, comments=None)
    numbers = []
    fieldmap = np.zeros(fields.shape, dtype=int)
    for i, row in enumerate(fields):
        numstr = ''
        for j, entry in enumerate(row):
            if entry in '0123456789':
                numstr += entry
                fieldmap[i, j] = len(numbers)
                continue
            if numstr:
                numbers.append(int(numstr))
                numstr = ''
            if entry == '.':
                fieldmap[i, j] = -1
            elif entry == '*':
                fieldmap[i, j] = -2
            else:
                fieldmap[i, j] = -3
        if numstr:
            numbers.append(int(numstr))
    return fieldmap, np.array(numbers)

def number_idcs(fieldmap):
    partnumbers = set()
    gearnums = []
    for i, j in zip(*np.where(fieldmap < -1)):
        region = fieldmap[max(i - 1, 0):i + 2, max(j - 1, 0):j + 2]
        partnums = set(region[region >= 0])
        partnumbers.update(partnums)
        if fieldmap[i, j] == -2 and len(partnums) == 2:
            gearnums.append(tuple(partnums))
    return np.array(list(partnumbers)), gearnums

def partnumbers(schematic):
    fieldmap, numbers = schematic
    return numbers[number_idcs(fieldmap)[0]]

def gearratios(schematic):
    fieldmap, numbers = schematic
    return [numbers[a] * numbers[b] for a, b in number_idcs(fieldmap)[1]]

if __name__ == '__main__':
    testschematic = load_schematic('testinput')
    schematic = load_schematic('input')

    assert sum(partnumbers(testschematic)) == 4361
    print(sum(partnumbers(schematic)))

    assert sum(gearratios(testschematic)) == 467835
    print(sum(gearratios(schematic)))
