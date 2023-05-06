import uuid
import json
import os.path

config_path = 'folder_dict.json'

def get_dict():
    folder_dict = {}
    if os.path.isfile(config_path):
        with open(config_path, 'r') as f:
            folder_dict = json.load(f) 
    return folder_dict

def update_dict(folder, value, folder_dict):
    pair = {folder : value}
    folder_dict.update(pair)
    return folder_dict

def convert_uuid(folder):
    """
    Converts a given folder dictionary to a new UUID value and updates it in a JSON file.

    Args:
        folder (dict): A dictionary representing the folder to update.

    Returns:
        str: The newly generated UUID value.
    """
    value = str(uuid.uuid4())
    folder_dict = update_dict(folder, value, get_dict())
    with open('folder_dict.json', 'w') as f:
        json.dump(folder_dict, f)
    return value

def query_uuid(folder):
    folder_dict = get_dict()
    return folder_dict[folder]