from textual.widgets import Static
from feetdb import FeetDB

class FeetModule(Static):
    """Display a basic text box"""

    DEFAULT_CSS = """
    FeetModule {
        width: 100%;
        height: 100%;
        padding: 0 0;
    }
    """

    def __init__(self, *args, db: FeetDB, host: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db = db
        self.host = host