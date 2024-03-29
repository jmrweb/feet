import subprocess
import jc

from textual.app import ComposeResult
from textual.widgets import Static, TextLog
from feetmodule import FeetModule
from modules.terminal import Terminal

class Portscan(FeetModule):
    """Run port scans against a host, show output in a text_box, and parse output to db."""

    DEFAULT_CSS = """
    Portscan {
        width: 100%;
        height: 100%;
        padding: 0 0;
        background: $panel;
        color: $text;
        border: $secondary hkey;
        border_title_align: center;
        content-align: center middle;
    }

    #options {
        padding: 0 0;
        background: $panel;
        color: $text;
        border: $secondary hkey;
        border_title_align: center;
        content-align: center middle;
    }

    
    """

    #_output = reactive("")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def compose(self) -> ComposeResult:
        yield Static("Options", id='options')
        #yield TextLog(id='output_log', highlight=True, markup=False)
        yield Terminal(db=self.db, host=self.host, id='nmap_tcp', title='NMAP TCP Port Scan', interactive=False)


    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""
        
        #Initialize TextLog
        #self.text_log = self.query_one(TextLog)

        #Set window title
        self.border_title = 'Port Scanner'
        self.query_one('#options').border_title = 'Options'
        #self.query_one('#output_log').border_title = 'Output Log'

        terminal = self.query_one('#nmap_tcp')
        cmd = ["nmap", "-p-", "-n", "127.0.0.1", "-oX", f"{self.host}_{terminal.id}.xml"]
        terminal.run_command(cmd)


    def parse_output(self, terminal: Terminal):
        """Parse output from nmap scan"""

        # parse xml to json
        xml_file = open(f"{self.host}_{terminal.id}.xml", "r")
        xml = xml_file.read()
        xml_file.close()
        data = jc.parse('xml', xml)

        #parse json to db
        for port in data['nmaprun']['host']['ports']['port']:
            # self.text_log.write(" ")
            self.db.conn.sadd(self.host + ':ports:index', port['@portid'])
            self.db.conn.hset(self.host + ':ports:' + port['@portid'], mapping={'protocol': port['@protocol']})
            
            #self.text_log.write("Protocol: " + port['@protocol'])
            if 'service' not in port:
                pass
            else:
                #self.text_log.write("Service: " + port['service']['@name'])
                self.db.conn.hset(self.host + ':ports:' + port['@portid'], mapping={'service': port['service']['@name']})
            #self.text_log.write("State: " + port['state']['@state'])
            self.db.conn.hset(self.host + ':ports:' + port['@portid'], mapping={'state': port['state']['@state']})


    def on_terminal_command_complete(self, message: Terminal.CommandComplete) -> None:
        """Called on a set interval to update command output"""
        self.parse_output(message.terminal)
