

import sys
#import inspect
import types

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import ContentSwitcher, Footer, Header, Label, Placeholder, Tabs, Tree

#import widgets
from widgets import *

NAMES = [
    "Paul Atreidies",
    "Duke Leto Atreides",
    "Lady Jessica",
    "Gurney Halleck",
    "Baron Vladimir Harkonnen",
    "Glossu Rabban",
    "Chani",
    "Stilgar",
]

class FeetApp(App):

    CSS_PATH = "feet.css"

    BINDINGS = [
    ("a", "add_tab", "Add tab"),
    ("r", "remove_tab", "Remove active tab"),
    ("c", "clear_tabs", "Clear tabs"),
    ("d", "disable_container", "Disable container"),
    ("e", "enable_container", "Enable container"),
]

    #def add_imported_widget(widget, widget_name: str) -> None:
    #    """Add a widget to the container"""
    #    #widget = getattr(sys.modules[__name__], widget_name)()
    #    widget = getattr(widget_name, widget_name)()
    #    new_widget = widget()
    #    self.query_one("widgets").mount(new_widget)

    #def get_imports() -> list:
    #    for name, val in globals().items():
    #        if isinstance(val, types.ModuleType):
    #            yield val.__name__

    tabbed_containers: dict
    widgets: list

    def add_imported_widgets(self) -> None:
        """Add imported widgets to the container"""
        for widget in self.widgets:
            self.action_add_imported_widget(widget)

    def action_add_tab(self) -> None:
        """Add a new tab."""
        tabs = self.query_one("#module_tabs1")

        # Cycle the names
        NAMES[:] = [*NAMES[1:], NAMES[0]]
        tabs.add_tab(NAMES[0])

    def action_add_imported_widget(self, widget_name: str) -> None:
        """Add a widget to the container"""
        module = __import__("widgets")
        widget = getattr(module, widget_name)
        widget_ = getattr(widget, widget_name.capitalize())
        new_widget = widget_()
        self.query_one("#container_main").mount(new_widget)

    def action_clear_tabs(self) -> None:
        """Clear the tabs."""
        self.query_one("#module_tabs").clear()

    def action_disable_container(self) -> None:
        """Disable the container."""
        self.query_one("#tab_container").visible = False

    def action_enable_container(self) -> None:
        """Enable the container."""
        self.query_one("#tab_container").visible = True

    def action_remove_imported_widget(self, widget_name: str) -> None:
        """Remove a widget from the container"""
        widget = getattr(sys.modules[__name__], widget_name)()
        self.query_one("widgets").unmount(widget)

    def action_remove_tab(self) -> None:
        """Remove active tab."""
        tabs = self.query_one("#module_tabs")
        active_tab = tabs.active_tab
        if active_tab is not None:
            tabs.remove_tab(active_tab.id)



    def get_widgets() -> list:
        for name, val in globals().items():
            if isinstance(val, types.ModuleType) and val.__name__.startswith('widgets'):
                yield val.__name__[8:]

    #def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
    #    """Handle TabActivated message sent by Tabs."""
    #    label = self.query_one(Label)
    #    if event.tab is None:
    #        # When the tabs are cleared, event.tab will be None
    #        label.visible = False
    #    else:
    #        label.visible = True
    #        label.update(event.tab.label)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="main"):
            with Horizontal(id="top_bar"):
                yield Placeholder("Placeholder 1", id="file", classes="menu")
                yield Placeholder("Placeholder 2", classes="menu")
                yield Tabs("192.168.0.11", "192.168.0.12", "192.168.0.13", id="ip_tabs")
            with Horizontal(id="modules_container1", classes="modules_container"):
                yield Tabs("nmap", "dirscan", id="module_tabs1", classes="module_tabs")
                yield Placeholder("Placeholder 3", id="placeholder_3", classes="module")
                yield Placeholder("Placeholder 4", id="placeholder_4", classes="module")


            # with Container(id="modules_container2", classes="modules_container"):
            #     yield Tabs(NAMES[0], id="module_tabs2", classes="module_tabs")
            #     yield Placeholder("Placeholder 5")
            #     yield Placeholder("Placeholder 6")
        yield Footer()
        #yield widgetselector.Widgetselector(self.widgets)
        #yield Container(widgetselector.Widgetselector(), id="container_main")
        #self.add_imported_widgets()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        pass
        # label = self.query_one(Label)
        # if event.tab is None:
        #     # When the tabs are cleared, event.tab will be None
        #     label.visible = False
        # else:
        #     label.visible = True
        #     label.update(event.tab.label)

    # get list of imported widgets
    widgets = list(get_widgets())

if __name__ == "__main__":

    #def print_classes():
    #    for name, obj in inspect.getmembers(sys.modules[__name__]):
    #        if inspect.isclass(obj):
    #            print(obj)

    #print_classes()

    # Print imported modules
    # print(sys.modules[__name__])

    #def get_imports() -> list:
    #    for name, val in globals().items():
    #        if isinstance(val, types.ModuleType):
    #            yield val.__name__

    #def get_widgets() -> list:
    #    for name, val in globals().items():
    #        if isinstance(val, types.ModuleType) and val.__name__.startswith('widgets'):
    #            yield val.__name__[8:]

    # get widgets from imports list
    #print(list(get_imports()))
    #widgets = [widget for widget in get_imports() if widget.startswith('widgets')]
    #print(widgets)
    #print(list(get_widgets()))
    #widgets = [widget for widget in get_widgets() if widget.startswith('widgets')]
    #widgets = list(get_widgets())
    #print(widgets)

    # Instantiate the app
    app = FeetApp()

    # start the app
    app.run()