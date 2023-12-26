
from itertools import cycle
import re

node_re = re.compile(r'(\w+) = \((\w+), (\w+)\)\n')

def load_maps(fname):
    nodes = {}
    with open(fname) as istream:
        directions = istream.readline().strip()
        # There is an empty line after the directions.
        istream.readline()
        for line in istream:
            m = node_re.fullmatch(line)
            nodes[m[1]] = (m[2], m[3])
    directions = [0 if d == 'L' else 1 for d in directions]
    return directions, nodes

def follow_maps(maps):
    directions, nodes = maps
    node = 'AAA'
    for n, d in enumerate(cycle(directions)):
        if node == 'ZZZ':
            break
        node = nodes[node][d]
    return n

def find_cycle(pos, directions, nodes):
    path = [(0, pos)]
    target = None
    for i, d in cycle(enumerate(directions, 1)):
        pos = nodes[pos][d]
        step = (i, pos)
        if step in path:
            break
        if pos.endswith('Z'):
            # This only happens once per path in the real input.
            # In the test input it happens twice and we want the last occurence.
            target = len(path)
        path.append(step)
    idx = path.index(step)
    return target, len(path) - idx

def gcd(a, b):
    if a > b:
        return gcd(b, a)
    c = b % a
    if c:
        return gcd(c, a)
    return a

def scm(a, b):
    return a * b // gcd(a, b)

def follow_ghostmaps(maps):
    directions, nodes = maps
    positions = [node for node in nodes if node.endswith('A')]
    n = 0
    mod = 1
    for pos in positions:
        target, cyclelen = find_cycle(pos, directions, nodes)
        while (n - target) % cyclelen or n < target:
            n += mod
        mod = scm(cyclelen, mod)
    return n

if __name__ == '__main__':
    testmaps = load_maps('testinput')
    testmaps2 = load_maps('testinput2')
    maps = load_maps('input')

    assert follow_maps(testmaps) == 2
    assert follow_maps(testmaps2) == 6
    print(follow_maps(maps))

    testmaps3 = load_maps('testinput3')

    assert follow_ghostmaps(testmaps3) == 6
    print(follow_ghostmaps(maps))
