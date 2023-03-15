from pathlib import Path
from textual.app import ComposeResult
from textual.messages import Message
from textual.reactive import reactive
from textual.widgets import Static, Button
#from . import *

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class Widgetselector(Static):
    """Display a list of widgets to select from"""

    DEFAULT_CSS = """
    Widgetselector {
        width: 40;
        height: 40;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
        content-align: center middle;
    }
    """
    widgets: list

    def __init__(self, widget_list: list) -> None:
        super().__init__()
        self.widgets = widget_list

    def on_mount(self) -> None:
        pass
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        #self.app.widget = button_id
        """Add a widget to the container"""
        module = __import__("widgets")
        widget = getattr(module, button_id)
        widget_ = getattr(widget, button_id.capitalize())
        #yield widget_()
        self.mount(widget_())

    def compose(self) -> ComposeResult:
        """Create buttons from the list of widgets"""
        for widget in self.widgets:
            yield Button(widget, id=widget)