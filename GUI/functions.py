from utils import Vector2D
from tkinter import filedialog, ttk
from configInterface.settings import current_settings
from PIL import Image
from configInterface.template import current_template



def select_folder() -> None:
    directory = filedialog.askdirectory()
    if directory:
        print(f"Selected directory: {directory}")
        current_settings.input_path = directory

def set_page_size(img_path: str) -> None:
    image = Image.open(img_path)
    current_template.page_dimensions = Vector2D(image.width, image.height)

def configure_aval() -> None:
    print("Configuring correction...")

#TODO
def on_finish() -> None:
    ...
