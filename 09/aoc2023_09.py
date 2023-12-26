
import numpy as np

def load_histories(fname):
    return np.loadtxt(fname, dtype=int)

def extrapolate(hist, *, previous=False):
    diffs = []
    while np.count_nonzero(hist):
        diffs.append(hist)
        hist = np.diff(hist)
    extra = [0]
    for diff in reversed(diffs):
        if previous:
            extra.append(diff[0] - extra[-1])
        else:
            extra.append(diff[-1] + extra[-1])
    return extra[-1]

def extrapolsum(histories, *, previous=False):
    return sum(extrapolate(hist, previous=previous) for hist in histories)

if __name__ == '__main__':
    testhists = load_histories('testinput')
    hists = load_histories('input')

    assert extrapolsum(testhists) == 114
    print(extrapolsum(hists))

    assert extrapolsum(testhists, previous=True) == 2
    print(extrapolsum(hists, previous=True))
