from textual import log
from feetmodule import FeetModule

class Hostinfo(FeetModule):
    """Display a basic text box"""

    DEFAULT_CSS = """
    Hostinfo {
        width: 40;
        height: 9;
        padding: 1 2;
        background: $panel;
        color: $text;
        border: $secondary tall;
        border_title_align: center;
        content-align: center middle;
    }
    """

    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""

        #Set window title
        self.border_title = "Host Information"

        # Print host info
        log(f"host:{self.host}")
        info = self.db.conn.hgetall(f"host:{self.host}")
        formatted_info = ""
        for k, v in info.items():
            formatted_info += f"{k} : {v} \n"
        self.update(formatted_info)