import sys
from GUI.main_window import CorretorGui
from configInterface.initializer import settings
from src.entry import entry_point


def args_entry_point(args: settings.properties_holder.properties) -> None:
    if args["debug"] is True:
        # Disable tracebacks
        sys.tracebacklimit = 0
    print(args)
    entry_point(args["input_paths"], args=args)


if __name__ == '__main__':
    app = CorretorGui()
    app.mainloop()

