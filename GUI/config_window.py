from configInterface.initializer import settings
from tkinter import ttk, filedialog
import tkinter as tk
from PIL import Image
from GUI.get_bubble_size import SelectMarkerSize

from utils import Vector2D


class ScannerConfig(tk.Toplevel):
    select_text: ttk.Label
    select_btn: ttk.Button
    adjust_text: ttk.Label
    adjust_btn: ttk.Button
    close_btn: ttk.Button

    def __init__(self):
        super().__init__()
        self.sheet_template_path: str = "Não Selecionado"
        self.title("Configuração")
        self.geometry("600x200")
        self.default()

    def default(self) -> None:
        # Configure grid layout for the container (self)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Ensure rows 0 and 1 (where labels are) expand vertically, but buttons don’t
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)  # Prevent Close button from stretching

        # Labels
        self.select_text = ttk.Label(self, text="Selecionar modelo de gabarito")
        self.select_text.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.adjust_text = ttk.Label(self, text="Ajustar tamanho das marcações")
        self.adjust_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Buttons (non-resizable vertically)
        self.select_btn = ttk.Button(self, text="Selecionar", command=self.get_template)
        self.select_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=5)  # `ew` prevents vertical stretching

        self.adjust_btn = ttk.Button(self, text="Ajustar", command=self.get_bubble_size)
        self.adjust_btn.grid(row=1, column=1, sticky="ew", padx=5, pady=5)  # `ew` prevents vertical stretching
        self.adjust_btn.configure(state=tk.DISABLED)

        # Close button (bottom-right, not stretching)
        self.close_btn = ttk.Button(self, text="Fechar", command=self.destroy)
        self.close_btn.grid(row=2, column=1, sticky="e", padx=10, pady=10)  # Only sticks to the right

    def get_template(self) -> None:
        self.sheet_template_path: str = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not self.sheet_template_path:
            return
        sheet_size: tuple[int, int] = Image.open(self.sheet_template_path).size
        settings.page_dimensions = Vector2D(sheet_size[0], sheet_size[1])
        self.update_adjust_button()

    def get_bubble_size(self):
        img_view: SelectMarkerSize = SelectMarkerSize(path_to_image=self.sheet_template_path)

    def update_adjust_button(self):
        self.adjust_btn.config(state=tk.NORMAL if self.sheet_template_path else tk.DISABLED)

