from pathlib import Path
from textual.message import Message
from textual.widgets import Button
from textual import log

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class MenuButton(Button):
    "Extend to send message to parent on loss of focus."

    class Blur(Message):
        "Message posted when a widget loses focus."

        def __init__(self, id: str) -> None:
            self.id = id
            super().__init__()

    def on_blur(self, event) -> None:
        "Hide menu on loss of focus."
        log("[bold_red]MenuButton on_blur triggered [/]")
        self.post_message(self.Blur(self.id))