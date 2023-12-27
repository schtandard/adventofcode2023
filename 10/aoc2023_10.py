
import numpy as np

segments = {
    '|': 'ns',
    '-': 'we',
    'L': 'ne',
    'J': 'nw',
    '7': 'sw',
    'F': 'se',
    '.': '',
}
directions = {
    'n': np.array([-1, 0]),
    's': np.array([1, 0]),
    'w': np.array([0, -1]),
    'e': np.array([0, 1]),
}
opposites = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

def load_pipes(fname):
    return np.genfromtxt(fname, dtype=str, delimiter=1)

def find_starttile(pipes):
    startcoords = np.array(*zip(*np.where(pipes == 'S')))
    sockets = []
    for d, step in directions.items():
        coords = startcoords - step
        if np.any((coords < 0) | (coords >= pipes.shape)):
            continue
        if d in segments[pipes[*coords]]:
            sockets.append(opposites[d])
    if len(sockets) != 2:
        raise ValueError("Coult not find start tile connections.")
    sockets = ''.join(sockets)
    tile = list(segments.keys())[list(segments.values()).index(sockets)]
    return startcoords, tile

def chase_step(pipes, pos, direction):
    newpos = pos + directions[direction]
    newdirection = segments[pipes[*newpos]].strip(opposites[direction])
    return newpos, newdirection

def mainloop(pipes):
    startpos, starttile = find_starttile(pipes)
    apos = bpos = startpos
    adir, bdir = segments[starttile]
    looptiles = np.zeros_like(pipes, dtype=str)
    looptiles[*apos] = starttile
    while True:
        apos, adir = chase_step(pipes, apos, adir)
        bpos, bdir = chase_step(pipes, bpos, bdir)
        looptiles[*apos] = pipes[*apos]
        looptiles[*bpos] = pipes[*bpos]
        if np.array_equal(apos, bpos):
            break
    return looptiles

def chaselen(pipes):
    looptiles = mainloop(pipes)
    return np.count_nonzero(looptiles) // 2

def count_enclosed(pipes):
    looptiles = mainloop(pipes)
    count = 0
    h, w = pipes.shape
    for i in range(h):
        n = s = False
        for j in range(w):
            if looptiles[i, j]:
                n ^= 'n' in segments[looptiles[i, j]]
                s ^= 's' in segments[looptiles[i, j]]
            elif n and s:
                count += 1
    return count

if __name__ == '__main__':
    testpipes = load_pipes('testinput')
    pipes = load_pipes('input')

    assert chaselen(testpipes) == 8
    print(chaselen(pipes))

    testpipes2 = load_pipes('testinput2')

    assert count_enclosed(testpipes2) == 10
    print(count_enclosed(pipes))
