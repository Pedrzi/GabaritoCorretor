from GUI.top_level_window import TopLevelWindow
from tkinter import ttk
import tkinter as tk
from configInterface.template import current_template
from GUI.functions import get_file_path

class ScannerConfig(TopLevelWindow):
    def __init__(self, title: str, root: tk.Tk):
        self.title: str = title
        self.root: tk.Tk = root

        super().__init__(root=self.root, title=self.title)

        self._close_button()
        ttk.Label(self.mainframe, text="Selecionar gabarito")
        self._create_button(0, "Selecionar", button_command=)

    def _close_button(self):
        close_button = ttk.Button(self.mainframe, text="Fechar", command=self.toplevel_window.destroy)
        close_button.grid(column=1, row=1, sticky=(tk.W, tk.E))



