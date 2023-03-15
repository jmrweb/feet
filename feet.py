

import sys
#import inspect
import types

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Tree

#import widgets
from widgets import *


class FeetApp(App):

    CSS_PATH = "feet.css"

    #def add_imported_widget(widget, widget_name: str) -> None:
    #    """Add a widget to the container"""
    #    #widget = getattr(sys.modules[__name__], widget_name)()
    #    widget = getattr(widget_name, widget_name)()
    #    new_widget = widget()
    #    self.query_one("widgets").mount(new_widget)

    def action_add_imported_widget(self, widget_name: str) -> None:
        """Add a widget to the container"""
        module = __import__("widgets")
        widget = getattr(module, widget_name)
        widget_ = getattr(widget, widget_name.capitalize())
        new_widget = widget_()
        self.query_one("#container_main").mount(new_widget)

    def add_imported_widgets(self) -> None:
        """Add imported widgets to the container"""
        for widget in self.widgets:
            self.action_add_imported_widget(widget)

    def action_remove_imported_widget(self, widget_name: str) -> None:
        """Remove a widget from the container"""
        widget = getattr(sys.modules[__name__], widget_name)()
        self.query_one("widgets").unmount(widget)
    
    #def get_imports() -> list:
    #    for name, val in globals().items():
    #        if isinstance(val, types.ModuleType):
    #            yield val.__name__

    def get_widgets() -> list:
        for name, val in globals().items():
            if isinstance(val, types.ModuleType) and val.__name__.startswith('widgets'):
                yield val.__name__[8:]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Horizontal(Tree(label="File", name="File_menu", id="file_menu"), Tree(label="192.168.0.0/24", name="Network_1", id="network_1"), id="top_row")
        yield Horizontal(Tree(label="Nmap"), Tree(label="Dir Scan"), id="second_row")
        yield Footer()
        #yield widgetselector.Widgetselector(self.widgets)
        #yield Container(widgetselector.Widgetselector(), id="container_main")
        #self.add_imported_widgets()

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