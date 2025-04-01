import tkinter as tk
from tkinter import ttk
from GUI.config_window import ScannerConfig
from GUI.widget_builder import  WidgetBuilder
import GUI.functions as functions

class CorretorGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Corretor de Gabarito")
        self.draw_widgets()

    def draw_widgets(self) -> None:
        # Configure grid layout
        self.columnconfigure(0, weight=1)  # Labels column
        self.columnconfigure(1, weight=1)  # Buttons column

        for i in range(3):
            self.rowconfigure(i, weight=1)  # Labels expand
        self.rowconfigure(3, weight=0)  # "Pronto" button should not stretch

        # Labels and buttons
        labels = [
            "Selecionar a pasta\ncom os arquivos de imagem",
            "Configurar scanner",
            "Configurar correção"
        ]
        commands = [
            functions.select_folder,
            ScannerConfig,
            functions.configure_aval
        ]

        for row, (label_text, command) in enumerate(zip(labels, commands)):
            ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="nsew", padx=5, pady=5)
            ttk.Button(self, text="Configurar" if row else "Selecionar", command=command).grid(row=row, column=1,
                                                                                               sticky="ew", padx=5,
                                                                                               pady=5)

        # "Pronto" button at the bottom-right
        ttk.Button(self, text="Pronto", command=functions.on_finish).grid(row=3, column=1, sticky="se", padx=10, pady=10)


if __name__ == "__main__":
    app = CorretorGui()
    app.mainloop()