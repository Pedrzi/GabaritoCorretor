import tkinter as tk
from tkinter import filedialog, ttk
from configInterface.settings import current_settings


def select_folder() -> None:
    directory = filedialog.askdirectory()
    if directory:
        print(f"Selected directory: {directory}")
        current_settings.input_path = directory

def get_file_path() -> str:
    file_path: str = filedialog.askopenfilename()
    return file_path

def get_page_size() -> None:
    image_path: str =


def configure_aval() -> None:
    print("Configuring correction...")

#TODO
def on_finish() -> None:
    ...
t