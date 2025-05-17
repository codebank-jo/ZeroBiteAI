import json  # Import the json module for parsing JSON files
import os    # Import the os module for file path operations

def load_inventory():
    # Construct the path to the inventory.json file located in the ../data directory
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory.json')
    # Open the JSON file in read mode
    with open(json_path, 'r') as f:
        data = json.load(f)  # Load the JSON data from the file into a Python dictionary
    # Extract and return the list under the "inventory" key from the loaded data
    return data["inventory"]