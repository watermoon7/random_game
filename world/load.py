import json

def load(world_name):
    with open(f"saves/{world_name}.json", 'r') as f:
        data = json.loads(f.read())
    return data

