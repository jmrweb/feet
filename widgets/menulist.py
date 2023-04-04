from pathlib import Path
from textual.message import Message
from textual.widgets import ListView
from textual import log

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class MenuList(ListView):
    "Extend ListView to default to visible=False on mount."

    # def __init__ (self, *children, visible: bool = False, **kwargs) -> None:
    #     self.visible = visible
    #     super().__init__(*children, **kwargs)
    
    def on_mount(self) -> None:
        "Set visible to False on mount."
        self.visible = False
        super().on_mount()
