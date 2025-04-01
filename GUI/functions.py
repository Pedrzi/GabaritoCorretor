from configInterface.initializer import settings
from tkinter import filedialog, ttk
from PIL import Image



def select_folder() -> None:
    directory = filedialog.askdirectory()
    if directory:
        print(f"Selected directory: {directory}")
        settings.input_path = directory

def configure_aval() -> None:
    print("Configuring correction...")

#TODO
def on_finish() -> None:
    ...
