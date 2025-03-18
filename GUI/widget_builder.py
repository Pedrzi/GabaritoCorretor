import tkinter as tk
from tkinter import ttk
from collections.abc import Callable


class WidgetBuilder(tk.Tk):
    def __init__(self, window = None):
        super().__init__()
        self.window = window

        if self.window is None:
            self.window = self

        self.mainframe: ttk.Frame = ttk.Frame(self.window, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.configure_layout()

    def create_label_and_button(self, row: int, label_text: str, button_text: str, button_command: Callable, column: int = 1) -> None:
        self.create_label(text=label_text, row=row)
        self.create_button(row=row, button_text=button_text, button_command=button_command, column=column)

    def create_label(self, text: str, row: int, column: int = 0):
        label = ttk.Label(self.mainframe, text=text)
        label.grid(column=0, row=row, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_button(self, row: int, button_text: str, button_command: Callable, column: int = 1) -> None:
        button = ttk.Button(self.mainframe, text=button_text, command=button_command)
        button.grid(column=column, row=row, sticky=(tk.W, tk.E), padx=5, pady=5)

    def configure_layout(self) -> None:
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)