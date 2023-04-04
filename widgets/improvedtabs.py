from pathlib import Path
from textual.widgets import Tabs, Tab
from rich.text import Text

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


class ImprovedTabs(Tabs):
    """Add improved funionality to the Tabs widget."""

    DEFAULT_CSS = """
    ImprovedTabs {
    }
    """
    def add_tab(self, tab: Tab | str | Text) -> None:
        """Add a new tab to the end of the tab list.

        Args:
            tab: A new tab object, or a label (str or Text).
        """
        from_empty = self.tab_count == 0
        tab_widget = (
            Tab(tab, id=f"tab-{self._new_tab_id}")
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