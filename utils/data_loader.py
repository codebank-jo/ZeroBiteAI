import json
import os

def load_inventory():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
    # Extract the list under the "inventory" key
    return data["inventory"]