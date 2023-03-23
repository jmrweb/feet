import sys
#import inspect
import types

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Button, ContentSwitcher, Footer, Header, Label, ListView, ListItem, Placeholder, Tab, Tabs
from textual import log
from textual import widget
from textual import events

#import 3rd party widgets
from widgets.menubutton import MenuButton
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
        # with Vertical(id="main"):
        #     with Horizontal(id="top_bar", classes="menu_bar"):
        #         yield Placeholder("File", id="file", classes="menu_button")
        #         yield Placeholder(" + ", id="add_host", classes="menu_button")
        #         with TabbedContent():
        #             yield Placeholder("File", id="file", classes="menu_button")
        #             yield Placeholder(" + ", id="add_host", classes="menu_button")
        #             with TabPane("192.168.0.11", id="ip192-168-0-11"):
        #                 with TabbedContent():
        #                     with TabPane("nmap", id="nmap"):
        #                         yield Placeholder("nmap", id="nmap", classes="module")
        #                     with TabPane("dirscan", id="dirscan"):
        #                         yield Placeholder("dirscan", id="dirscan", classes="module")
        #             with TabPane("192.168.0.12", id="ip192-168-0-12"):
        #                 with TabbedContent():
        #                     with TabPane("wpscan", id="wpscan"):
        #                         yield Placeholder("wpscan", id="wpscan", classes="module")
        #                     with TabPane("ffuf", id="ffuf"):
        #                         yield Placeholder("ffuf", id="ffuf", classes="module")
                    
        with Vertical(id="main"):
            with Horizontal(id="top_bar", classes="menu_bar"):
                yield MenuButton("File", id="file_menu_button", classes="menu_button")
                yield Button("Network", id="network_menu_button", classes="menu_button")
                yield Placeholder(" + ", id="add_host_button", classes="menu_button")
                yield Tabs(
                    Tab("192.168.0.11", id="ip192-168-0-11"),
                    Tab("192.168.0.12", id="ip192-168-0-12"),
                    id="ip_tabs",
                )
            yield ListView(
                ListItem(Label("Open")),
                ListItem(Label("Save")),
                ListItem(Label("Save As")),
                ListItem(Label("Exit")),
                initial_index=None, id="file_menu_list",
            )
            # yield ListView(
            #     ListItem(Label("add network")),
            #     ListItem(Label("remove network")),
            #     ListItem(Label("clear networks")),
            #     ListItem(Label("192.168.0.0/24")),
            #     ListItem(Label("192.168.1.0/24")),
            #     ListItem(Label("192.168.255.255/24")),
            #     initial_index=None, id="network_menu_list",
            # )
            with ContentSwitcher(id="ip_switcher"):
                with Vertical(id="ip192-168-0-11", classes="modules_container"):
                    with Horizontal(classes="menu_bar"):
                        yield Placeholder(" + ", id="add_module_button", classes="menu_button")
                        yield Tabs(
                            Tab("nmap", id="nmap"),
                            Tab("dirscan", id="dirscan"),
                            id="module_tabs", classes="module_tabs",
                        )
                    with ContentSwitcher(id="module_switcher"):
                        yield Placeholder("nmap", id="nmap", classes="module")
                        yield Placeholder("dirscan", id="dirscan", classes="module")
                with Vertical(id="ip192-168-0-12", classes="modules_container"):
                    with Horizontal(classes="menu_bar"):
                        yield Placeholder(" + ", id="add_module_button", classes="menu_button")
                        yield Tabs(
                            Tab("wpscan", id="wpscan"),
                            Tab("ffuf", id="ffuf"),
                            id="module_tabs", classes="module_tabs",
                        )
                    with ContentSwitcher(id="module_switcher"):
                        yield Placeholder("wpscan", id="wpscan", classes="module")
                        yield Placeholder("ffuf", id="ffuf", classes="module")
        yield Footer()
        #yield widgetselector.Widgetselector(self.widgets)
        #yield Container(widgetselector.Widgetselector(), id="container_main")
        #self.add_imported_widgets()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle ButtonPressed message sent by Button."""
        if event.button.id == "file_menu_button":
            if self.query_one("#file_menu_list").visible == False:
                self.query_one("#file_menu_list").visible = True
            elif self.query_one("#file_menu_list").visible == True:
                self.query_one("#file_menu_list").visible = False
        else:
            log(f"[bold_red]on_button_pressed: [/] Unknown button: {event.widget.id}")

    # def on_descendant_blur(self, event: events.DescendantBlur) -> None:
    #     """Handle Blur message sent by Button."""
    #     if event.handler_name == "file_menu_button":
    #         self.query_one("#file_menu_list").visible = False
    #     else:
    #         log(f"[bold_red]on_descendant_blur: [/] Unknown event: {event.handler_name}")

    def on_click(self, event: events.Click) -> None:
        """Hide menus when mouse is clicked outside of them."""
        self.query_one("#file_menu_list").visible = False

    # def on_menu_button_blur(self, message: MenuButton.Blur):
    #     """Handle Blur message sent by MenuButton."""
    #     log(f"[bold_red]on_tabs_tab_activated: [/] MessageID: {message.id}")
    #     if message.id == "file_menu_button":
    #         self.query_one("#file_menu_list").visible = False

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        if event.tabs.id == "ip_tabs":
            self.query_one("#ip_switcher").current = event.tab.id
        elif event.tabs.id == "module_tabs":
            event.tabs.parent.parent.query_one(ContentSwitcher).current = event.tab.id
        else:
            log(f"[bold_red]on_tabs_tab_activated: [/] Parent Tabs: {event.tabs.id}")
            log(f"[bold_red]on_tabs_tab_activated: [/] Parent ContentSwitcher: {event.tabs.parent.parent.query_one(ContentSwitcher)}")
        
        
        
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