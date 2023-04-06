import sys
#import inspect
import types

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, ContentSwitcher, Footer, Header, Input, Label, ListView, ListItem, Placeholder, Static
from textual import log
from textual import events

#import 3rd party widgets
from widgets.menubutton import MenuButton
from widgets.menulist import MenuList
from widgets.improvedtabs import ImprovedTabs, ImprovedTab
from widgets import *

class HostContainer(Vertical):

    DEFAULT_CSS = """
        HostContainer {
        }    
    """

    def add_module(self, module_name: str) -> None:
        moduleid = module_name
        new_module = Placeholder(moduleid, id=moduleid, classes="module")
        # module_switcher = self.query_one("#module_switcher")
        # mount_await = module_switcher.mount(new_module)
        mount_await = self.query_one("#module_switcher").mount(new_module)

        async def refresh_active() -> None:
            """Wait for module to be mounted before making active."""
            await mount_await
            new_tab = ImprovedTab(moduleid, id=moduleid)
            module_tabs = self.query_one("#module_tabs")
            module_tabs.focus()
            module_tabs.add_tab(new_tab)
        
        self.call_after_refresh(refresh_active)
        
        #module_tabs.active = moduleid
        # module_switcher.active = moduleid
        # module_tabs._activate_tab(new_tab)


    def compose(self) -> ComposeResult:
        # Render the widget
        with Horizontal(classes="menu_bar"):
            yield MenuButton(" + ", id="add_module_button", classes="menu_button")
            yield ImprovedTabs(
                ImprovedTab("nmap", id="nmap"),
                ImprovedTab("dirscan", id="dirscan"),
                id="module_tabs", classes="module_tabs",
            )
        yield MenuList(
            ListItem(Label("dirscan"), id="dirscan"),
            ListItem(Label("ffuf"), id="ffuf"),
            ListItem(Label("nmap"), id="nmap"),
            ListItem(Label("wpscan"), id="wpscan"),
            initial_index=None, id="add_module_list"
        )
        with ContentSwitcher(id="module_switcher"):
            yield Placeholder("nmap", id="nmap", classes="module")
            yield Placeholder("dirscan", id="dirscan", classes="module")


class HostInput(Static):
    # A widget to input new hosts addresses

    DEFAULT_CSS = """
        HostInput {
            width: 24;
            max-width: 24;
            height: 5;
            border: $secondary tall;
            border_title_align: center;
            content-align: center middle;
        }
    """

    def add_host(self, ip) -> None:
        ipid = "ip" + ip.replace(".", "-")
        #host_tabs = self.parent.query_one("#host_tabs")
        #host_tabs.add_tab(ImprovedTab(ip, id=ipid))
        new_container = HostContainer(id=ipid, classes="modules_container")
        # host_switcher = self.parent.query_one("#host_switcher")
        # host_switcher.mount(new_container)
        #host_tabs.active = ipid

        mount_await = self.parent.query_one("#host_switcher").mount(new_container)
        
        async def refresh_active() -> None:
            """Wait for module to be mounted before making active."""
            await mount_await
            new_tab = ImprovedTab(ip, id=ipid)
            host_tabs = self.parent.query_one("#host_tabs")
            host_tabs.focus()
            host_tabs.add_tab(new_tab)
        self.call_after_refresh(refresh_active)
    
        self.visible=False

    def compose(self) -> ComposeResult:
        # Render the widget
        yield Input(placeholder="127.0.0.1")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Called when a button is pressed
        self.add_host(event.value)

    def on_mount(self) -> None:
        # Called when the widget is mounted
        self.border_title = "Add Host"
        self.visible = False


class FeetApp(App):

    CSS_PATH = "feet.css"

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

    def action_add_imported_widget(self, widget_name: str) -> None:
        """Add a widget to the container"""
        module = __import__("widgets")
        widget = getattr(module, widget_name)
        widget_ = getattr(widget, widget_name.capitalize())
        new_widget = widget_()
        self.query_one("#container_main").mount(new_widget)

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

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)
        yield HostInput(id="host_input")
        with Vertical(id="main"):
            with Horizontal(id="top_bar", classes="menu_bar"):
                yield MenuButton("File", id="file_menu_button", classes="menu_button")
                yield Button("Network", id="network_menu_button", classes="menu_button")
                yield Button(" + ", id="add_host_button", classes="menu_button")
                yield ImprovedTabs(
                    ImprovedTab("192.168.0.11", id="ip192-168-0-11"),
                    ImprovedTab("192.168.0.12", id="ip192-168-0-12"),
                    id="host_tabs",
                )
            yield MenuList(
                ListItem(Label("Open"), id="Open"),
                ListItem(Label("Save"), id="Save"),
                ListItem(Label("Save As", id="Save As")),
                ListItem(Label("Exit"), id="Exit"),
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
            with ContentSwitcher(id="host_switcher"):
                yield HostContainer(id="ip192-168-0-11", classes="modules_container")
                yield HostContainer(id="ip192-168-0-12", classes="modules_container")
        yield Footer()
        #yield widgetselector.Widgetselector(self.widgets)
        #yield Container(widgetselector.Widgetselector(), id="container_main")
        #self.add_imported_widgets()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        
        # Handle buttonPressed message.

        # Handle ButtonPressed message sent by add_host_button.
        if event.button.id == ("add_host_button"):
            host_input = self.query_one("#host_input")                   
            host_input.visible = True
            host_input.query_one("Input").focus()
        
        # Handle ButtonPressed message sent by file_menu_button.
        elif event.button.id == "file_menu_button":
            file_menu_list = self.query_one("#file_menu_list")                   
            if file_menu_list.visible is False:
                file_menu_list.visible = True
            elif file_menu_list.visible is True:
                file_menu_list.visible = False

        # Handle ButtonPressed message sent by add_module_button.
        elif event.button.id == "add_module_button":
            add_module_list = event.button.parent.parent.query_one("#add_module_list")                
            if add_module_list.visible is False:
                add_module_list.visible = True
            elif add_module_list.visible is True:
                add_module_list.visible = False

        # Log error if unknown button is pressed.
        else:
            log(f"[bold_red]on_button_pressed: [/] Unknown button: {event.button.id}")

    # def on_descendant_blur(self, event: events.DescendantBlur) -> None:
    #     """Handle Blur message sent by Button."""
    #     if event.handler_name == "file_menu_button":
    #         self.query_one("#file_menu_list").visible = False
    #     else:
    #         log(f"[bold_red]on_descendant_blur: [/] Unknown event: {event.handler_name}")

    def on_click(self, event: events.Click) -> None:
        # Hide menus when mouse is clicked outside of them.
        log("[bold_red]App on_click triggered [/]")
        for menu in self.query("MenuList"):
            menu.visible = False

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # Handle ListView.Selected message sent by ListView.

        # Log selected ListItem.
        log(f"[bold_red]on_list_view_selected: [/] {event.item.id}")

        if event.item.id == "Exit":
            exit()
        elif event.item.parent.id == "add_module_list":
            event.item.parent.parent.add_module(event.item.id)

    def on_menu_button_blur(self, message: MenuButton.Blur):
        # Handle Blur message.
        
        log(f"[bold_red]on_mwnu_button_blur_activated: [/] MessageID: {message.button.id}")
        
        # Handle blur message sent by file_menu_button.
        if message.button.id == "file_menu_button":                     
            self.query_one("#file_menu_list").visible = False
        # Handle blur message sent by add_module_button.
        elif message.button.id == "add_module_button":                  
            message.button.parent.parent.query_one("#add_module_list").visible = False
        

    def on_tabs_tab_activated(self, event: ImprovedTabs.TabActivated) -> None:
        # Handle TabActivated message sent by ImprovedTabs.

        if event.tabs.id == "host_tabs":
            self.query_one("#host_switcher").current = event.tab.id
        elif event.tabs.id == "module_tabs":
            event.tabs.parent.parent.query_one(ContentSwitcher).current = event.tab.id
        else:
            log(f"[bold_red]on_tabs_tab_activated: [/] Parent ImprovedTabs: {event.tabs.id}")
            log(f"[bold_red]on_tabs_tab_activated: [/] Parent ContentSwitcher: {event.tabs.parent.parent.query_one(ContentSwitcher)}")
        
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