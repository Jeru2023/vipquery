import uuid
import json
import os.path
from PyPDF2 import PdfReader


class folder_updater:
    def __init__(self, config_path='folder_dict.json'):
        self.config_path = config_path

    def get_dict(self):
        folder_dict = {}
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                folder_dict = json.load(f)
        return folder_dict

    def get_key_list(self):
        return self.get_dict().keys()

    def update_dict(self, folder, value, folder_dict):
        pair = {folder: value}
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

    def create_folder(self, folder_name):
        """
            create a folder
        """
        # folder_dict = self.get_dict()
        new_folder_path = os.path.join("./upload/", self.convert_uuid(folder_name))
        os.mkdir(new_folder_path)
        # self.update_dict()

    def is_pdf_file(file_path):
        try:
            with open(file_path, "rb") as file:
                # Read the first 4 bytes of the file
                file_signature = file.read(4)

                # Compare the read bytes to the PDF signature
                if file_signature == b'%PDF':
                    print(f"PDF file found: {file_path}")
                    return True
                else:
                    return False
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return False

    def save_files(self, folder_name, file_name, bytes_data):
        print(f"上传目录为：{folder_name},文件名：{file_name}")
        upload_folder = self.query_uuid(folder_name)
        file_path= f'./upload/{upload_folder}/{file_name}'
        with open(file_path, 'wb+') as f:
            f.write(bytes_data)
        with open(file_path, "rb") as file:
            file_signature = file.read(4)
        if file_signature == b'%PDF':
            reader = PdfReader(file_path)
            raw_text = ''
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    raw_text += text
            name, extension = os.path.splitext(file_name)
            # Replace the extension with '.txt'
            new_file_name = name + '.txt'
            new_file_name = f'./upload/{upload_folder}/{new_file_name}'
            with open(new_file_name, 'w', encoding='utf-8') as txtfile:
                txtfile.write(raw_text)
                txtfile.close()


