
import numpy as np

cube_kinds = {"red": 0, "green": 1, "blue": 2}

def load_games(fname):
    games = {}
    with open(fname) as istream:
        for line in istream:
            game, moves = line.strip().split(": ")
            game = int(game.removeprefix("Game "))
            moves = moves.split("; ")
            cubes = []
            for move in moves:
                cubes.append(np.zeros(3, dtype=int))
                for group in move.split(", "):
                    num, kind = group.split(" ")
                    cubes[-1][cube_kinds[kind]] += int(num)
            games[game] = np.array(cubes)
    return games

def possible_sum(games, cubes):
    cubes = np.array(cubes)
    return sum(game for game in games if not np.any(games[game] > cubes))

def minpower_sum(games):
    return sum(moves.max(0).prod() for moves in games.values())

if __name__ == '__main__':
    testgames = load_games('testinput')
    games = load_games('input')

    assert possible_sum(testgames, [12, 13, 14]) == 8
    print(possible_sum(games, [12, 13, 14]))

    assert minpower_sum(testgames) == 2286
    print(minpower_sum(games))
