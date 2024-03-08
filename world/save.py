import json


def save(world_name, world_data, player):
    """
    Saves the world to a textfile

    Format:
        {
          "chunks": {
            "chunk_00": {
              "grass":
            }
          },
          "player": {
            "pos": [330,555],
            "velocity": [0,37.12800000000001],
            "acceleration": [0,2400],
            "jump": true,
            "grounded": true,
            "speed": 1650,
            "inventory": {}
          }
        }
    """
    with open("world/world_data.txt", 'r+') as f:
        worlds = [i for i in f.read().split("\n") if i]
        if world_name not in worlds:
            f.write(f"{world_name}\n")

    data = {
        "chunks": world_data,
        "player": player
    }

    with open(f"saves/{world_name}.json", 'w') as file:
        json.dump(data, file, indent=4)
