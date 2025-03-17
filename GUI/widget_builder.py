import tkinter as tk
from tkinter import ttk
from collections.abc import Callable


class WidgetBuilder:
    def __init__(self, root: tk.Tk, title: str, window = None):

        self.window = window
        self.title: str = title
        self.root: tk.Tk = root
        self.root.title(self.title)


        if self.window is None:
            self.window = self.root

        self.mainframe: ttk.Frame = ttk.Frame(self.window, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self._configure_layout()

    def _create_label_and_button(self, row: int, label_text: str, button_text: str, button_command: Callable) -> None:
        label = ttk.Label(self.mainframe, text=label_text)
        label.grid(column=0, row=row, sticky=(tk.W, tk.E))

        button = ttk.Button(self.mainframe, text=button_text, command=button_command)
        button.grid(column=1, row=row, sticky=(tk.W, tk.E))

    def _create_button(self, row: int, button_text: str, button_command: Callable, column: int = 1) -> None:
        button = ttk.Button(self.mainframe, text=button_text, command=button_command)
        button.grid(column=column, row=row, sticky=(tk.W, tk.E))

    def _configure_layout(self) -> None:
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)