import json

data = {
    "chunks": {
        "chunk_00": {
            "grass": [(0, 0), (0, 1), (2, 0)],
            "stone": [(0, 2), (0, 3), (1, 0), (1, 1)]
        }
    },
    "player": {
        "pos": [0, 0],
        "speed": 1650,
        "inventory": ["sword", "pickaxe", "iron_sword"]
    }
}


def write():
    with open('tests/test.json', 'w') as f:
        json.dump(data, f, indent=4)


def read():
    with open('tests/test.json', 'r') as f:
        res = json.load(f)
    return res


write()
print(read())
