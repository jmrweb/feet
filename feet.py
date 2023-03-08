from widgets import *

import sys
import inspect

from textual.app import App


class Feet(App):
    pass

if __name__ == "__main__":

    def print_classes():
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                print(obj)

    #print_classes()

    # Print imported modules
    #print(sys.modules[__name__])

    # Print imported modules
    import types
    def imports():
        for name, val in globals().items():
            if isinstance(val, types.ModuleType):
                yield val.__name__

    print(list(imports()))

    # Instantiate the app
    #app = App()

    # start the app
    #app.run()