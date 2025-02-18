import os
import pathlib
import shutil
import streamlit as st
import time
from google.genai import types
import mimetypes
from functools import wraps
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def detect_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def read_file(filepath: str) -> types.Part:
    try:
        data_bytes = types.Part.from_bytes(
            data=pathlib.Path(filepath).read_bytes(),
            mime_type=detect_mime_type(filepath),
        )
        return data_bytes
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        st.error("Failed to read file. Please try again.")
        return None


def clear_directory(folder_path: str = "files") -> None:
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")


def create_directory(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        st.write("Took: %2.4f sec" % (te - ts))
        return result

    return wrap