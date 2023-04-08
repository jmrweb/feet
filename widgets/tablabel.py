from __future__ import annotations

from pathlib import Path
from textual.message import Message
from textual.widgets import Label
from textual import log

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

class TabLabel(Label):
    """Label for ImprovedTab widget."""

    class Clicked(Message):
        """Message posted when TabLabel is clicked."""

        def __init__(self, label: TabLabel) -> None:
            self.label = label
            super().__init__()

    def on_click(self):
        # generate Clicked message on on_click
        log("[bold_red]TabLable clicked.[/]")
        self.post_message(TabLabel.Clicked(self))