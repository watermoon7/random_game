import json

def save(world_name, world_data, player):
    """Saves the world in a textfile"""
    with open("world/world_data.txt", 'r+') as file:
        worlds = [i for i in file.read().split("\n") if i]
        if world_name not in worlds:
            file.write(f"{world_name}\n")

    data = {
        "world": world_data,
        "player": player
    }

    with open(f"saves/{world_name}.json", 'w') as file:
        json.dump(data, file, indent=4)
