import uuid
import json
import os.path

config_path = 'folder_dict.json'

def get_folder_dict():
    folder_dict = {}
    if os.path.isfile(config_path):
        with open(config_path, 'r') as f:
            folder_dict = json.load(f) 
    return folder_dict

def update_dict(key, folder, folder_dict):
    pair = {key : folder}
    folder_dict.update(pair)
    return folder_dict

def convert_uuid(folder):
    # map uuid and folder name, persist localy
    key = str(uuid.uuid4())
    folder_dict = update_dict(key, folder, get_folder_dict())
    with open('folder_dict.json', 'w') as f:
        json.dump(folder_dict, f)
    return key

convert_uuid('abc2')