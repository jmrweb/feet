from pathlib import Path
from textual.widgets import Static
from feetmodule import FeetModule

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class Basicwidget(FeetModule):
    """Display a basic text box"""

    DEFAULT_CSS = """
    Basicwidget {
        width: 40;
        height: 9;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
        content-align: center middle;
    }
    """
    def on_mount(self) -> None:
        self.update("Hello World!")