from rich.highlighter import ReprHighlighter
from rich.pretty import Pretty
from rich.protocol import is_renderable
from rich.text import Text

from textual.app import ComposeResult
from textual.widgets import Tree
from textual.widgets.tree import TreeNode
from feetmodule import FeetModule

from textual import log

class Hostinfo(FeetModule):
    """Display a basic text box"""

    DEFAULT_CSS = """
    Hostinfo {
        width: 100%;
        height: 100%;
        padding: 0 0;
        background: $panel;
        color: $text;
        border: $secondary hkey;
        border_title_align: center;
        content-align: center middle;
    }
    """


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info_tree = None
        self.highlighter = ReprHighlighter()

        # Subcribe to redis keyspace notifications
        self.pubsub = self.db.conn.pubsub()
        #self.pubsub.psubscribe('__keyspace@0__:*')
        self.pubsub.psubscribe(f"__keyspace@{self.db.dbindex}__:{self.host}:*")

        # Set update timer
        self.update_timer = self.set_interval(1/60, self.update_module, pause=True)
    

    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree(f'Host: {self.host}')
        tree.root.expand()
        yield tree

   
    def initialize_tree(self):
        """Populate tree with initial values"""

        #Add info to tree
        keys = self.db.conn.keys(f'{self.host}:*')
        for key in keys:
            split_key = key.split(':', 1)[1]
            split_key = split_key.split(':')
            if not split_key[len(split_key)-1] == 'index':
                branch = self.info_tree.root
                
                while split_key:
                    branch_key = split_key.pop(0).capitalize()
                    children = branch.children
                    branch_exists = False
                    for child in children:
                        if str(child.label) == branch_key:
                            branch = child
                            branch_exists = True
                            break
                    if not branch_exists:
                        label = self.render_text(branch_key)
                        branch = branch.add(label, expand=True)

                key_info = self.db.conn.hgetall(key)
                for k, v in key_info.items():
                    label = self.render_text(f'{k}: {v}')
                    branch.add_leaf(label)


    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""

        #Set window title
        self.border_title = "Host Information"

        #Initialize tree
        self.info_tree = self.query_one(Tree)
        self.initialize_tree()

        #Start update timer
        self.update_timer.resume()


    def render_text(self, text: str) -> Text:
        """Render text with rich"""
        if not is_renderable(text):
            renderable = Pretty(text)
        else:
            renderable = Text.from_markup(text)
            renderable = self.highlighter(text)
        return renderable

    def update_tree(self, message: dict):
        """Update tree with new info"""

        #Get key from message
        key = message['channel'].split(':', 1)[1]
        split_key = key.split(':', 1)[1]
        split_key = split_key.split(':')

        #Add info to tree
        if not split_key[len(split_key)-1] == 'index':
            branch = self.info_tree.root
            while split_key:
                branch_key = split_key.pop(0).capitalize()
                children = branch.children
                branch_exists = False
                for child in children:
                    if str(child.label) == branch_key:
                        branch = child
                        branch_exists = True
                        break
                if not branch_exists:
                    label = self.render_text(branch_key)
                    branch = branch.add(label, expand=True)

            children = branch.children
            key_info = self.db.conn.hgetall(key)
            for child in children:
                if key_info.items():
                    k, v = key_info.popitem()
                    label = self.render_text(f'{k}: {v}')
                    child.label = label
                    self.info_tree.refresh_line(child.line)
                else:
                    break
            while key_info.items():
                k, v = key_info.popitem()
                label = self.render_text(f'{k}: {v}')
                branch.add_leaf(label)


    def update_module(self) -> None:
        """Called on a set interval to update module"""
        if self.db.connected:
            message = self.pubsub.get_message()
            if message:
                if message['type'] == 'pmessage':
                    key = message['channel'].split(':', 1)[1]
                    split_key = key.split(':')
                    if not split_key[len(split_key)-1] == 'index':
                        self.update_tree(message)