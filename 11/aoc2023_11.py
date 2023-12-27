
import numpy as np

def load_sky(fname):
    galaxies = np.genfromtxt(fname, dtype=str, delimiter=1, comments=None)
    return galaxies.shape, np.where(galaxies == '#')

def expanded(sky, *, factor=2):
    (h, w), (yy, xx) = sky
    xx = xx.copy()
    yy = yy.copy()
    for y in range(h, -1, -1):
        if y not in yy:
            yy[yy > y] += factor - 1
            h += factor - 1
    for x in range(w, -1, -1):
        if x not in xx:
            xx[xx > x] += factor - 1
            w += factor - 1
    return (h, w), (yy, xx)

def distsum(sky, *, factor=2):
    sky = expanded(sky, factor=factor)
    _, (yy, xx) = sky
    dsum = 0
    for m in range(len(yy)):
        for n in range(m + 1, len(yy)):
            dsum += abs(xx[m] - xx[n]) + abs(yy[m] - yy[n])
    return dsum

if __name__ == '__main__':
    testsky = load_sky('testinput')
    sky = load_sky('input')

    assert distsum(testsky) == 374
    print(distsum(sky))

    assert distsum(testsky, factor=10) == 1030
    assert distsum(testsky, factor=100) == 8410
    print(distsum(sky, factor=1000000))
