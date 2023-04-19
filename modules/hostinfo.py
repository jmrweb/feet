from textual.app import ComposeResult
from textual.widgets import Tree
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

        # Subcribe to redis keyspace notifications
        self.pubsub = self.db.conn.pubsub()
        self.pubsub.psubscribe('__keyspace@0__:*')
        #self.pubsub.psubscribe(f"__keyspace@{self.db.dbindex}__:{self.host}:*")

        # Set update timer
        #self.update_timer = None
        self.update_timer = self.set_interval(1/60, self.update_module, pause=True)
    

    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree(f'Host: {self.host}')
        tree.root.expand()
        yield tree


    def get_leaf(self, split_key: list)
         """Recursively search tree for leaf"""
            log(f"Searching for leaf: {split_key}")
            log(f"Current node: {node}")
            log(f"Current node children: {node.children}")
            if len(split_key) == 0:
                return node
            else:
                for child in node.children:
                    if child.label == split_key[0].capitalize():
                        return self.get_leaf(split_key[1:], child)
                    else:
                        return self.get_leaf(split_key[1:], node)
                    


   def initialize_tree(self):
        """Populate tree with initial values"""

        #Add info to tree
        keys = self.db.conn.keys(f'{self.host}:*')
        for key in keys:
            split_key = key.split(':')
            if not split_key[len(split_key)-1] == 'index':
                branch = self.info_tree.root.add(split_key[len(split_key)-1].capitalize(), expand=True)
                key_info = self.db.conn.hgetall(key)
                for k, v in key_info.items():
                    branch.add_leaf(f'{k}: {v}')

        log(f"Tree parsing")
        log(self.info_tree.root)
        for child in self.info_tree.root.children:
            log("Child:")
            log(child.label)
            log(child.id)
        #log(self.info_tree[0])
        #log(self.info_tree.root.children)
        #log(self.info_tree.root.children[0])


    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""

        #Set window title
        self.border_title = "Host Information"

        #Initialize tree
        self.info_tree = self.query_one(Tree)
        self.initialize_tree()

        #Update info in text_log
        #self.update__info()

        #Start update timer
        self.update_timer.resume()

    def update_tree(self, message: dict):
        log(f"Updating tree")
        log(message)

        key = message['channel'].split(':', 1)[1]
        split_key = key.split(':')
        #key_host = message['channel'].split(':')[1]
        #key_branch = message['channel'].split(':')[2]
        log(f"Key: {key}")
        log(f"Split key: {split_key}")
        if split_key[0] == self.host and not split_key[len(split_key)-1] == 'index':
          if message['data'] == 'hset' or message['data'] == 'sadd':
            get_leaf()
            

                
            #recursively update tree nodes
            #self.info_tree.root[split_key].


    #     """Update text_log with host info"""
    #     #Clear text_log
    #     self.text_log.clear()

    #     #Print host info to text_log        
    #     self.text_log.write("General:")
    #     self.text_log.write(" ")
    #     info = self.db.conn.hgetall(f'{self.host}:general')
    #     for k, v in info.items():
    #         self.text_log.write(f"\t {k} : {v}")
    #     self.text_log.write(" ")

    #     #Print port info to text_log
    #     self.text_log.write("Ports:")
    #     self.text_log.write(" ")
    #     if not self.db.conn.exists(self.host + ':ports'):
    #         self.text_log.write("\t No open ports discovered.")
    #     else:
    #         ports = self.db.conn.sort(self.host + ':ports')
    #         for port in ports:
    #             self.text_log.write(f"\t Port: {port}")
    #             info = self.db.conn.hgetall(self.host + ':' + port)
    #             for k, v in info.items():
    #                 self.text_log.write(f"\t {k} : {v}")
    #             self.text_log.write(" ")


    def update_module(self) -> None:
        """Called on a set interval to update module"""
        if self.db.connected:
            message = self.pubsub.get_message()
            if message:
                #pass
                self.update_tree(message)
            #self.text_log.write(message)

        #self.text_log.write("No message")
        
        #Check for redis keyspace notifications
        # for message in self.pubsub.get_message():
        #     self.text_log.write(message)
            #self.update_info()