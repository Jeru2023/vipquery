import os
import streamlit as st

BASE_DIR = 'upload'

def save_uploaded_file(file, folder):
    folder_path = os.path.join(BASE_DIR, folder)
    with open(os.path.join(folder_path, file.name), "wb") as f:
        f.write(file.getbuffer())
    return st.success(f"Saved File: {file.name} to {folder_path}")
