from pathlib import Path
from textual.app import ComposeResult
from textual.widgets import Button, ListView, ListItem, Static

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

class Dropdownmenu(Static):
    """Display a drop down menu using textual ListView"""

    DEFAULT_CSS = """
    /* Dropdownmenu {
        width: 40;
        height: 9;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
        content-align: center middle;
    } */

    ListView {
        height: auto;

    }
    """
    menu_list: ListView()

    def __init__(
        self, *children: ListItem,
        initial_index: int | None = 0,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    )-> None:
        """
        Args:
            *children: The ListItems to display in the list.
            initial_index: The index that should be highlighted when the list is first mounted.
            name: The name of the widget.
            id: The unique ID of the widget used in CSS/query selection.
            classes: The CSS classes of the widget.
            disabled: Whether the ListView is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.menu_list = ListView(*children, initial_index=initial_index)


    def compose(self) -> ComposeResult:
        "Create child widgets of a drop down menu."
        yield Button()
        yield ListItem()