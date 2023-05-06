import uuid
import json

with open('folder_dict.json','r') as f:
    folder_dict = json.load(f)
def update_dict(key, folder):
    pair = {key : folder}
    folder_dict.update(pair)
    return folder_dict

def convert_uuid(folder):
    # map uuid and folder name, persist localy
    key = str(uuid.uuid4())
    folder_dict = update_dict(key, folder)
    with open('folder_dict.json', 'w') as f:
        json.dump(folder_dict, f)
    return key