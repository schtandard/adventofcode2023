
import numpy as np

def import_highscores(fname):
    with open(fname) as istream:
        times = np.fromstring(istream.readline().strip('Time: \n'),
                              dtype=int, sep=' ')
        dists = np.fromstring(istream.readline().strip('Distance: \n'),
                              dtype=int, sep=' ')
    return np.vstack((times, dists)).T

def numwinstrats(time, record):
    recordtime = (time - np.sqrt(time*time - 4 * record)) / 2
    return time - 1 - 2 * int(recordtime)

def errormargin(highscores):
    return np.prod([numwinstrats(*race) for race in highscores])

def unkern(highscores):
    time = dist = ''
    for t, d in highscores:
        time += str(t)
        dist += str(d)
    return [[int(time), int(dist)]]

if __name__ == '__main__':
    testscores = import_highscores('testinput')
    scores = import_highscores('input')

    assert errormargin(testscores) == 288
    print(errormargin(scores))

    testscores = unkern(testscores)
    scores = unkern(scores)

    assert errormargin(testscores) == 71503
    print(errormargin(scores))
