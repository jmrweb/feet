from pathlib import Path
from textual.widgets import ListView

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class MenuList(ListView):
    """Extend ListView to default to visible=False on mount."""

    def on_mount(self) -> None:
        """Set visible to False on mount."""
        self.visible = False
        super().on_mount()
