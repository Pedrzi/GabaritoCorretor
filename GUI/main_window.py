import tkinter as tk

from GUI.config_window import ScannerConfig
from GUI.widget_builder import  WidgetBuilder
import GUI.functions as functions

class CorretorGui(WidgetBuilder):
    def __init__(self):
        super().__init__()
        self.title("Corretor de Gabarito")
        self._create_widgets()

    def _create_widgets(self) -> None:
        self.create_label_and_button(
            row=0,
            label_text="Selecionar a pasta\ncom os arquivos de imagem",
            button_text="Selecionar",
            button_command=functions.select_folder
        )
        self.create_label_and_button(
            row=1,
            label_text="Configurar scanner",
            button_text="Configurar",
            button_command=ScannerConfig
        )
        self.create_label_and_button(
            row=2,
            label_text="Configurar correção",
            button_text="Configurar",
            button_command=functions.configure_aval
        )
        self.create_button(
            row=3,
            button_text="Pronto",
            button_command=functions.on_finish
        )




if __name__ == "__main__":
    app = CorretorGui()
    app.mainloop()