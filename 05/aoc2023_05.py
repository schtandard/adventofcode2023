
def load_almanac(fname, *, ranged=False):
    with open(fname) as istream:
        line = istream.readline()
        seeds = [int(s) for s in line.strip('seeds: \n').split(' ')]
        if ranged:
            seeds = [(start, start + rlen)
                     for start, rlen in zip(seeds[::2], seeds[1::2])]
        else:
            seeds = [(start, start + 1) for start in seeds]
        mappings = []
        istream.readline() # empty line
        istream.readline() # first map header
        mapranges = []
        for line in istream:
            if line == '\n':
                mappings.append(make_mapping(mapranges))
                istream.readline() # map header
                mapranges = []
                continue
            mapranges.append(tuple(int(s) for s in line.strip().split(' ')))
        mappings.append(make_mapping(mapranges))
    return sorted(seeds), mappings

def make_mapping(mapranges):
    mapranges = sorted([(src, src + rangelen, dest - src)
                        for dest, src, rangelen in mapranges])
    def mapping(valranges):
        mapped = []
        viter = iter(valranges)
        miter = iter(mapranges)
        try:
            vstart, vstop = next(viter)
            mstart, mstop, mdiff = next(miter)
            while True:
                if not vstart < vstop:
                    vstart, vstop = next(viter)
                if vstop <= mstart:
                    mapped.append((vstart, vstop))
                    vstart, vstop = next(viter)
                    continue
                if vstart >= mstop:
                    mstart, mstop, mdiff = next(miter)
                    continue
                if vstart < mstart:
                    mapped.append((vstart, mstart))
                    vstart = mstart
                thisstop = min(vstop, mstop)
                mapped.append((vstart + mdiff,
                               thisstop + mdiff))
                vstart = thisstop
        except StopIteration:
            if vstart < vstop:
                mapped.append((vstart, vstop))
            for v in viter:
                mapped.append(v)
        return sorted(mapped)
    return mapping

def process_almanac(almanac):
    vals, mappings = almanac
    for mapping in mappings:
        vals = mapping(vals)
    return vals

def minloc(almanac):
    locs = process_almanac(almanac)
    return locs[0][0]

if __name__ == '__main__':
    testalmanac = load_almanac('testinput')
    almanac = load_almanac('input')

    assert minloc(testalmanac) == 35
    print(minloc(almanac))

    testalmanac = load_almanac('testinput', ranged=True)
    almanac = load_almanac('input', ranged=True)

    assert minloc(testalmanac) == 46
    print(minloc(almanac))
