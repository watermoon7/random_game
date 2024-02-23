import random
import numpy as np

def generate_terrain(width, height, smoothness, values):
    """Generates and returns a 2-dimensional list which represents the terrain

    Args:
        width: the width of the terrain
        height: the height of the terrain
        smoothness: how many times the smoothening algorithm is applied
        values: a dictionary containing the values to be spread throughout the terrain

    Returns:
        A 2-D list representing the generated terrain
    """

    terrain = [[None for _ in range(width)] for _ in range(height)]

    create_noise(terrain, values)

    for _ in range(smoothness):
        smooth(terrain, values)

    return terrain

def create_noise(terrain, values):
    for i in range(len(terrain)):
        for j in range(len(terrain[0])):
            terrain[i][j] = choose_value(values)

def choose_value(values):
    choice = random.random() * sum(values.values())

    threshold = 0
    for value in values:
        threshold += values[value]
        if choice < threshold:
            return value

def smooth(terrain, values):
    indices = []
    for i in range(len(terrain)):
        for j in range(len(terrain[0])):
            indices.append((i, j))

    random.shuffle(indices)

    for i in indices:
        row, col = i
        neighbors = get_neighbors(terrain, i)

        terrain[row][col] = determine_value(neighbors, values)

def get_neighbors(terrain, pos):
    adjacent = (
        (-1, -1), ( 0, -1), ( 1, -1),
        (-1,  0), ( 0,  0), ( 1,  0),
        (-1,  1), ( 0,  1), ( 1,  1)
    )
    neighbors = []
    for adj in adjacent:
        new_pos = np.add(pos, adj)

        if 0 <= new_pos[0] < len(terrain) and 0 <= new_pos[1] < len(terrain[0]):
            neighbors.append(terrain[new_pos[0]][new_pos[1]])

    return neighbors

def determine_value(neighbors, values):
    counts = sorted([(value, neighbors.count(value)) for value in values], key=lambda x: x[1])
    new = [i for i in counts if i[1] == counts[-1][1]]
    return random.choice(new)[0]


def generate_chunk(width, height, cell_size):
    world_top = generate_terrain(width//cell_size, height//(8*cell_size), 0, {' ': 1})
    layer1 = generate_terrain(width//cell_size, height//(4*cell_size), 1, {'g':1.3, ' ': 1})
    layer2 = generate_terrain(width//cell_size, 5*height//(8*cell_size), 3, {'g':1, ' ': 1})
    chunk = world_top + layer1 + layer2
    for _ in range(3):
        smooth(chunk, {'g':1, ' ': 1})
    return chunk
