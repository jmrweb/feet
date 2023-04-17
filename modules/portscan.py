import subprocess
import jc

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import TextLog
from feetmodule import FeetModule

class Portscan(FeetModule):
    """Display a basic text box"""

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
    """

    _output = reactive("")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running_cmd = False
        self._running_scan = False
        self._process = None
        self.text_log = None
        self.update_timer = self.set_interval(1/60, self.update__output, pause=True)


    def compose(self) -> ComposeResult:
        yield TextLog(highlight=True, markup=False)

    def parse_output(self):
        """Parse output from nmap scan"""
        xml_file = open(f"{self.host}_nmap.xml", "r")
        xml = xml_file.read()
        xml_file.close()
        data = jc.parse('xml', xml)

        self.text_log.write("Parsed Output")
        # self.text_log.write(data['nmaprun']['host']['ports']['port'])
        for port in data['nmaprun']['host']['ports']['port']:
            self.text_log.write(" ")
            self.text_log.write("Port: " + port['@portid'])
            self.text_log.write("Protocol: " + port['@protocol'])
            self.text_log.write("Service: " + port['service']['@name'])
            self.text_log.write("State: " + port['state']['@state'])
        

    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""
        
        #Initialize TextLog
        self.text_log = self.query_one(TextLog)

        #Set window title
        self.border_title = "Output Log"

        # Print test data
        # text_log = self.query_one(TextLog)
        # cmd = ["cat", "/etc/passwd"]
        # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        # for line in proc.stdout:
        #     text_log.write(line)
        # text_log.write("[bold magenta]Write text or any Rich renderable!")

        cmd = ["nmap", "-p-", "-n", "127.0.0.1", "-oX", f"{self.host}_nmap.xml"]
        self.run_command(cmd)

    def run_command(self, cmd: str):
        """Start process for a cli command"""

        # Start output update timer
        self.update_timer.resume()
        
        # Execute command
        self._process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        # text_log = self.query_one(TextLog)
        # process = subprocess.Popen(command, stdout=subprocess.PIPE)
        # while True:
        #     output = process.stdout.readline()
        #     if len(output) == 0 and process.poll() is not None:
        #         break
        #     if output:
        #         text_log.write(output.strip())
        # rc = process.poll()
        # return rc

    def update__output(self) -> None:
        """Called on a set interval to update command output"""

        if len(self._output) == 0 and self._process.poll() is not None:
            self.text_log.write("Command finished.")
            self.update_timer.pause()

            self.parse_output()
        else:
            self._output = self._process.stdout.readline()

    def watch__output(self, output: str) -> None:
        """Called when the command output updates"""
        self.text_log.write(str(output)[2:-3])
