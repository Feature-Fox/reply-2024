import itertools
import os.path
from typing import Tuple

from app import parse_file, visualize_grid

instructions = {
    "3": [("left", "right")],
    "5": [("down", "right")],
    "6": [("left", "down")],
    "7": [("left", "right"), ("left", "down"), ("down", "right")],
    "9": [("up", "right")],
    "96": [("left", "down"), ("up", "right")],
    "A": [("left", "up")],
    "A5": [("left", "up"), ("down", "right")],
    "B": [("left", "right"), ("left", "up"), ("up", "right")],
    "C": [("up", "down")],
    "C3": [("left", "right"), ("up", "down")],
    "D": [("up", "down"), ("up", "right"), ("down", "right")],
    "E": [("left", "up"), ("left", "down"), ("up", "down")],
    "F": [("left", "right"), ("left", "down"), ("left", "up"), ("up", "down"), ("down", "right"), ("up", "right")],
}
tiles = []


def find_shortest_path(golden_points):
    min_distance = float('inf')
    shortest_path = []
    for permutation in itertools.permutations(golden_points):
        distance = 0
        for i in range(len(permutation) - 1):
            distance += abs(permutation[i][0] - permutation[i + 1][0]) + abs(permutation[i][1] - permutation[i + 1][1])
        if distance < min_distance:
            min_distance = distance
            shortest_path = permutation
    print('min_distance:', min_distance)
    return shortest_path


def step_by_step(position, destination):
    path = []
    path_names = []

    distance = (destination[0] - position[0], destination[1] - position[1])
    if abs(distance[0]) > abs(distance[1]):
        if distance[0] > 0:
            path_names.append(("left", "right"))
        else:
            path_names.append(("right", "left"))
    else:
        if distance[1] > 0:
            path_names.append(("up", "down"))
        else:
            path_names.append(("down", "up"))

    while position != destination:
        distance = (destination[0] - position[0], destination[1] - position[1])
        if abs(distance[0]) + abs(distance[1]) == 1:
            print('break, lol?')
        if abs(distance[0]) > abs(distance[1]):
            if distance[0] > 0:
                position = (position[0] + 1, position[1])
                tile_name = check_tile((get_start_dir(path_names[-1][1]), "right"))
                path.append(f'{tile_name} {position[0]} {position[1]}')
                path_names.append((get_start_dir(path_names[-1][1]), "right"))
            else:
                position = (position[0] - 1, position[1])
                tile_name = check_tile((get_start_dir(path_names[-1][1]), "left"))
                path.append(f'{tile_name} {position[0]} {position[1]}')
                path_names.append((get_start_dir(path_names[-1][1]), "left"))
        else:
            if distance[1] > 0:
                position = (position[0], position[1] + 1)
                tile_name = check_tile((get_start_dir(path_names[-1][1]), "down"))
                path.append(f'{tile_name} {position[0]} {position[1]}')
                path_names.append((get_start_dir(path_names[-1][1]), "down"))
            else:
                position = (position[0], position[1] - 1)
                tile_name = check_tile((get_start_dir(path_names[-1][1]), "up"))
                path.append(f'{tile_name} {position[0]} {position[1]}')
                path_names.append((get_start_dir(path_names[-1][1]), "up"))
        print('position:', position)
    print(path)
    print(path_names)

    return path


def get_start_dir(end_dir: str):
    if end_dir == "right":
        return "left"
    if end_dir == "left":
        return "right"
    if end_dir == "up":
        return "down"
    if end_dir == "down":
        return "up"


def check_tile(move: Tuple):
    global tiles
    for i, (tile_name, score, tile_count) in enumerate(tiles):
        if tile_count > 0:
            if any(move[0] in t and move[1] in t for t in instructions[tile_name]):
                print(f'Tile: {tile_name}, {move=}, {score}')
                tiles[i] = (tile_name, tiles[i][1], tiles[i][2] - 1)
                return tile_name
    raise Exception("no way")


def calculate(path):
    full_output = []
    for i in range(len(path) - 1):
        print(f'path: {path[i]} {path[i + 1]} \n')
        full_output.extend(step_by_step(path[i], path[i + 1]))
    return full_output


def main():
    global tiles
    file_names = ['00-trailer.txt',
                  # '01-comedy.txt', '02-sentimental.txt',
                  # '03-adventure.txt', '04-drama.txt', '05-horror.txt'
                  ]
    if not os.path.exists('../output'):
        os.makedirs('../output')

    for file_name in file_names:
        grid = parse_file('../data/' + file_name)
        tiles = grid['tiles']
        path = find_shortest_path(grid['golden_points'])
        visualize_grid(grid)
        full_output = calculate(path)
        with open(os.path.join('../output/', file_name), 'w', newline='') as file:
            for line in full_output:
                file.write(f'{line}\n')


if __name__ == '__main__':
    main()
