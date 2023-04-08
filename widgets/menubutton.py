from __future__ import annotations

from pathlib import Path
from textual.message import Message
from textual.widgets import Button
from textual import log

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class MenuButton(Button):
    "Extend Button widget to send a message to parent (including copy of button) on loss of focus."

    DEFAULT_CSS = """
    Button {
        width: auto;
        min-width: 1;
        height: 1;
        background: $panel;
        color: $text;
        border: none;
        /* border-top: none; */
        /* border-bottom: solid; */
        content-align: center middle;
        text-style: bold;
        padding: 0 0 0 0;
        margin: 0 0 0 0;
    }

    Button:focus {
        text-style: bold reverse;
    }

    Button:hover {
        border-top: none;
        background: $panel-darken-2;
        color: $text;
    }

    Button.-active {
        background: $panel;
        border-bottom: tall $panel-lighten-2;
        border-top: tall $panel-darken-2;
        tint: $background 30%;
    }

    /* Primary variant */
    Button.-primary {
        /* background: $primary; */
        color: $text;
        /* border-top: tall $primary-lighten-3; */
        /* border-bottom: tall $primary-darken-3; */
        /* padding: 0 0 0 0; */

    }

    Button.-primary:hover {
        background: $primary-darken-2;
        color: $text;
        border-top: tall $primary-lighten-2;
    }

    Button.-primary.-active {
        background: $primary;
        border-bottom: tall $primary-lighten-3;
        border-top: tall $primary-darken-3;
    }


    /* Success variant */
    Button.-success {
        background: $success;
        color: $text;
        border-top: tall $success-lighten-2;
        border-bottom: tall $success-darken-3;
    }

    Button.-success:hover {
        background: $success-darken-2;
        color: $text;
    }

    Button.-success.-active {
        background: $success;
        border-bottom: tall $success-lighten-2;
        border-top: tall $success-darken-2;
    }


    /* Warning variant */
    Button.-warning {
        background: $warning;
        color: $text;
        border-top: tall $warning-lighten-2;
        border-bottom: tall $warning-darken-3;
    }

    Button.-warning:hover {
        background: $warning-darken-2;
        color: $text;

    }

    Button.-warning.-active {
        background: $warning;
        border-bottom: tall $warning-lighten-2;
        border-top: tall $warning-darken-2;
    }


    /* Error variant */
    Button.-error {
        background: $error;
        color: $text;
        border-top: tall $error-lighten-2;
        border-bottom: tall $error-darken-3;

    }

    Button.-error:hover {
        background: $error-darken-1;
        color: $text;

    }

    Button.-error.-active {
        background: $error;
        border-bottom: tall $error-lighten-2;
        border-top: tall $error-darken-2;
    }

    """

    class Blur(Message):
        "Message posted when a widget loses focus."

        def __init__(self, button: MenuButton) -> None:
            self.button = button
            super().__init__()

    def on_blur(self) -> None:
        "Hide menu on loss of focus."
        log("[bold_red]MenuButton on_blur triggered [/]")
        self.post_message(MenuButton.Blur(self))
        