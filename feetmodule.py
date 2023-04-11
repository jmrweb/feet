from rich.console import RenderableType

from textual.widgets import Static
from feetdb import FeetDB

class FeetModule(Static):
    """Display a basic text box"""

    DEFAULT_CSS = """
    FeetModule {
    }
    """

    def __init__(
        self,
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        db: FeetDB,
        host: str,
    ) -> None:
        super().__init__(renderable=renderable, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
        self.db = db
        self.host= host