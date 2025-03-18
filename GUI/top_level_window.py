import tkinter as tk
from tkinter import  ttk
from GUI.widget_builder import WidgetBuilder

class TopLevelWindow(WidgetBuilder):
    def __init__(self):
        self.toplevel_window: tk.Toplevel = tk.Toplevel()
        super().__init__(window=self.toplevel_window)




