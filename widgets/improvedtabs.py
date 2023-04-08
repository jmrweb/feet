from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual import events
from textual import log
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Label, ListItem, Static, Tabs, Tab
from rich.text import Text, TextType


from widgets.menubutton import MenuButton
from widgets.tabclosebutton import TabCloseButton
from widgets.tablabel import TabLabel

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

class ImprovedTab(Tab):
    """Add improved functionality to the ImprovedTab widget."""

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

    Horizontal {
        width: auto;
        height: 1;
        padding: 0 0 0 0;
        margin: 0 0 0 0;
    }

    .close_button {
        background: red;
        color: white;
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
    #     """Initialise a ImprovedTab.

    #     Args:
    #         label: The label to use in the tab.
    #         id: Optional ID for the widget.
    #     """
    #     self.label = Text.from_markup(label) if isinstance(label, str) else label
    #     #super().__init__(id=id)
    #     #self.update(label)

    class CloseTab(Message):
        # Message posted when TabCloseButton is clicked.
        
        def __init__(self, tab: ImprovedTab) -> None:
            self.tab = tab
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        with Horizontal():
            yield TabLabel(self.label.plain, id="tab_label")
            yield TabCloseButton("X", classes="close_button")
            # yield ListItem(Label("X", classes="close_button"))
            #yield Button("X", classes="close_button")

    def on_click(self):
        pass

    def on_tab_close_button_clicked(self, message: TabCloseButton.Clicked):
        """Inform the message that the TabCloseButton was clicked."""
        self.post_message(self.CloseTab(self))

    def on_tab_label_clicked(self, message: TabLabel.Clicked) -> None:
        """Inform the message that the tab was clicked."""
        self.post_message(self.Clicked(self))

    def on_mount(self) -> None:
        self.update()

class ImprovedTabs(Tabs):
    """Add improved functionality to the Tabs widget."""

    DEFAULT_CSS = """
    Tabs {
        width: 100%;
        height:2;
    }
    Tabs > #tabs-scroll {
        height: 2;
        overflow: hidden;
    }
    Tabs #tabs-list-bar {
        width: auto;
        height: 2;
        min-width: 100%;
        overflow: hidden hidden;
    }
    Tabs #tabs-list {
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

    def add_tab(self, tab: ImprovedTab | str | Text) -> None:
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

    async def _on_tab_clicked(self, event: ImprovedTab.Clicked) -> None:
        """Activate a tab that was clicked."""
        self.focus()
        event.stop()
        try:
            self._activate_tab(event.tab)
        except ValueError:
            pass

    def on_improved_tab_close_tab(self, message: ImprovedTab.CloseTab) -> None:
        """Handle the tab being closed."""
        self.remove_tab(message.tab.id)

    # def remove_tab(self, tab_or_id: ImprovedTab | str | None) -> None:
    #     """Remove a tab.

    #     Args:
    #         tab_id: The ImprovedTab's id.
    #     """
    #     if tab_or_id is None:
    #         return
    #     if isinstance(tab_or_id, ImprovedTab):
    #         remove_tab = tab_or_id
    #     else:
    #         try:
    #             remove_tab = self.query_one(f"#tabs-list > #{tab_or_id}", ImprovedTab)
    #         except NoMatches:
    #             return
    #     removing_active_tab = remove_tab.has_class("-active")

    #     next_tab = self._next_active
    #     if next_tab is None:
    #         self.post_message(self.Cleared(self))
    #     else:
    #         self.post_message(self.TabActivated(self, next_tab))

    #     async def do_remove() -> None:
    #         """Perform the remove after refresh so the underline bar gets new positions."""
    #         await remove_tab.remove()
    #         if removing_active_tab:
    #             if next_tab is not None:
    #                 next_tab.add_class("-active")
    #             self.call_after_refresh(self._highlight_active, animate=True)

    #     self.call_after_refresh(do_remove)