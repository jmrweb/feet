from textual.app import ComposeResult
from textual.widgets import TextLog
from feetmodule import FeetModule

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
        self.text_log = None

        # Subcribe to redis keyspace notifications
        self.pubsub = self.db.conn.pubsub()
        self.pubsub.psubscribe('__keyspace@0__:*')
        #self.pubsub.psubscribe(f"__keyspace@{self.db.dbindex}__:{self.host}:*")

        # Set update timer
        #self.update_timer = None
        self.update_timer = self.set_interval(1/60, self.update_module, pause=True)
    

    def compose(self) -> ComposeResult:
        yield TextLog(highlight=True, markup=True)


    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""

        #Set window title
        self.border_title = "Host Information"

        #Initialize text_log
        self.text_log = self.query_one(TextLog)

        #Update info in text_log
        #self.update__info()

        #Start update timer
        self.update_timer.resume()
    

    def update__info(self):
        """Update text_log with host info"""
        #Clear text_log
        self.text_log.clear()

        #Print host info to text_log        
        self.text_log.write("General:")
        self.text_log.write(" ")
        info = self.db.conn.hgetall(f"host:{self.host}")
        for k, v in info.items():
            self.text_log.write(f"\t {k} : {v}")
        self.text_log.write(" ")

        #Print port info to text_log
        self.text_log.write("Ports:")
        self.text_log.write(" ")
        if not self.db.conn.exists(self.host + ':ports'):
            self.text_log.write("\t No open ports discovered.")
        else:
            ports = self.db.conn.sort(self.host + ':ports')
            for port in ports:
                self.text_log.write(f"\t Port: {port}")
                info = self.db.conn.hgetall(self.host + ':' + port)
                for k, v in info.items():
                    self.text_log.write(f"\t {k} : {v}")
                self.text_log.write(" ")


    def update_module(self) -> None:
        """Called on a set interval to update module"""
        message = self.pubsub.get_message()
        if message:
            self.update__info()
            #self.text_log.write(message)
        #self.text_log.write("No message")
        
        #Check for redis keyspace notifications
        # for message in self.pubsub.get_message():
        #     self.text_log.write(message)
            #self.update_info()