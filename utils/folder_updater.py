import uuid
import json
import os.path

class folder_updater:
    def __init__(self, config_path='folder_dict.json'):
        self.config_path = config_path
    
    def get_dict(self):
        folder_dict = {}
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                folder_dict = json.load(f) 
        return folder_dict

    def update_dict(self, folder, value, folder_dict):
        pair = {folder : value}
        folder_dict.update(pair)
        return folder_dict

    def convert_uuid(self, folder):
        """
        Converts a given folder dictionary to a new UUID value and updates it in a JSON file.

        Args:
            folder (dict): A dictionary representing the folder to update.

        Returns:
            str: The newly generated UUID value.
        """
        value = str(uuid.uuid4())
        folder_dict = self.update_dict(folder, value, self.get_dict())
        with open(self.config_path, 'w') as f:
            json.dump(folder_dict, f)
        return value

    def query_uuid(self, folder):
        folder_dict = self.get_dict()
        return folder_dict[folder]