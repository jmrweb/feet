from pathlib import Path
from textual.app import ComposeResult
from textual.widgets import Static, Button, Label, Tabs, Tab
from rich.text import Text, TextType

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

class ImprovedTab(Tab):
    """Add improved functionality to the Tab widget."""



    # ImprovedTab.-active {
    #     text-style: bold;
    #     color: $text;
    # }
    
    # ImprovedTab:hover {
    #     text-style: bold;
    # }
    
    # ImprovedTab.-active:hover {
    #     color: $text;
    # }
    
    DEFAULT_CSS = """

    ImprovedTab {
        width: auto;
        height: 1;
        padding: 0 0 0 0;
        text-align: center;
        color: $text-disabled;
    }
    ImprovedTab.-active {
        text-style: bold;
        color: $text;
    }
    ImprovedTab:hover {
        text-style: bold;
    }
    ImprovedTab.-active:hover {
        color: $text;
    }
    
    ImprovedTab #tab_label {
        margin: 0 0 0 0;
        padding: 0 0 0 1;
        height: 1;
    }

    .close_button {
        /* align-horizontal: right; */
        background: red;
        color: white;
        /* text-align: center; */
        height: 1;
        width: 1;
        padding: 0 0 0 0;
        margin: 0 0 0 0;
    }
    """

    # def __init__(
    #     self,
    #     label: TextType,
    #     *,
    #     id: str | None = None,
    # ) -> None:
    #     """Initialise a Tab.

    #     Args:
    #         label: The label to use in the tab.
    #         id: Optional ID for the widget.
    #     """
    #     self.label = Text.from_markup(label) if isinstance(label, str) else label
    #     #super().__init__(id=id)
    #     #self.update(label)

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield Label(self.label.plain, id="tab_label")
        yield Button(" + ", classes="close_button")

    def on_mount(self) -> None:
        self.update()

class ImprovedTabs(Tabs):
    """Add improved functionality to the Tabs widget."""

    DEFAULT_CSS = """
    ImprovedTabs {
        width: 100%;
        height:2;
    }
    ImprovedTabs > #tabs-scroll {
        height: 2;
        overflow: hidden;
    }
    ImprovedTabs #tabs-list-bar {
        width: auto;
        height: 2;
        min-width: 100%;
        overflow: hidden hidden;
    }
    ImprovedTabs #tabs-list {
        min-height: 1;
        width: auto;
        height: 1;
        min-width: 100%;
        overflow: hidden hidden;
    }

    Underline {
        height: 1;
        padding: 0 0 0 0;
        margin: 0 0 0 0;
    }

    ImprovedTabs:focus .underline--bar {
        background: $foreground 20%;
    }
    """

    def add_tab(self, tab: Tab | str | Text) -> None:
        """Add a new tab to the end of the tab list.

        Args:
            tab: A new tab object, or a label (str or Text).
        """
        from_empty = self.tab_count == 0
        tab_widget = (
            ImprovedTab(tab, id=f"tab-{self._new_tab_id}")
            if isinstance(tab, (str, Text))
            else self._auto_tab_id(tab)
        )
        mount_await = self.query_one("#tabs-list").mount(tab_widget)

        if from_empty:
            tab_widget.add_class("-active")
            self.post_message(self.TabActivated(self, tab_widget))

            async def refresh_active() -> None:
                """Wait for things to be mounted before highlighting."""
                await mount_await
                self.active = tab_widget.id or ""
                self._highlight_active(animate=False)

            self.call_after_refresh(refresh_active)
        
        else:
            async def refresh_active() -> None:
                """Wait for things to be mounted before highlighting."""
                await mount_await
                self._activate_tab(tab_widget)
            
            self.call_after_refresh(refresh_active)