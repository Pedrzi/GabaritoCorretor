import tkinter as tk
from tkinter import  ttk
from GUI.widget_builder import WidgetBuilder

class TopLevelWindow(WidgetBuilder):
    def __init__(self, title: str, root: tk.Tk):
        self.toplevel_window: tk.Toplevel = tk.Toplevel(self.root)
        super().__init__(root=root, title=title, window=self.toplevel_window)




