import tkinter as tk

from GUI.config_window import ScannerConfig
from GUI.widget_builder import  WidgetBuilder
import GUI.functions as functions

class CorretorGui(WidgetBuilder):
    def __init__(self, root):
        super().__init__(root, title="Corretor Gabarito")
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._create_label_and_button(
            row=0,
            label_text="Selecionar a pasta\ncom os arquivos de imagem",
            button_text="Selecionar",
            button_command=functions.select_folder
        )
        self._create_label_and_button(
            row=1,
            label_text="Configurar scanner",
            button_text="Configurar",
            button_command=self._open_scanner_config
        )
        self._create_label_and_button(
            row=2,
            label_text="Configurar correção",
            button_text="Configurar",
            button_command=functions.configure_aval
        )
        self._create_button(
            row=3,
            button_text="Pronto",
            button_command=functions.on_finish
        )

    def _open_scanner_config(self) -> None:
        ScannerConfig(title="Configuração", root=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = CorretorGui(root)
    root.mainloop()