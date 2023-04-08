from __future__ import annotations

from pathlib import Path
from textual.message import Message
from textual.widgets import Static
from textual import log

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

class TabCloseButton(Static):
    """A button that closes the tab."""

    class Clicked(Message):
        """ Message posted when TabCloseButton is clicked. """

        def __init__(self, button: TabCloseButton) -> None:
            self.button = button
            super().__init__()

    def on_click(self) -> None:
        """Handle click event."""

        # log(f"Closing tab: {self.parent.parent.id}")
        # log(f"Related tabs: {self.parent.parent.parent.parent.parent.parent}")

        # tab = self.parent.parent
        # log(f"Closing tab: {self.parent.parent.id}")
        # tabs = self.parent.parent.parent.parent.parent.parent
        # log(f"Tabs: {tabs.id}")

        # tabs.remove_tab(tab.id)

        # generate Clicked message on on_click
        #log("[bold_red]TabCloseButton clicked.[/]")
        log("[bold_red]TabCloseButton clicked.[/]")
        self.post_message(TabCloseButton.Clicked(self))

    def on_mount(self) -> None:
        """Mount the TabCloseButton."""
        self.update("X")