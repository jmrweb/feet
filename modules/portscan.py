import subprocess

from rich.syntax import Syntax

from textual import log
from textual.app import App, ComposeResult
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

    output = reactive("")
    running_scan = False
    _process = None

    def compose(self) -> ComposeResult:
        yield TextLog(highlight=False, markup=False)

    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""
        
        #Set window title
        self.border_title = "Output Log"

        #Start output update timer
        self.set_interval(1/60, self.update_output)

        # Print test data
        text_log = self.query_one(TextLog)

        cmd = ["cat", "/etc/passwd"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for line in proc.stdout:
            text_log.write(line)
        
        text_log.write("[bold magenta]Write text or any Rich renderable!")

        cmd = ["nmap", "-p-", "-n", "127.0.0.1"]
        self.running_scan = True
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        # process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        # while True:
        #     output = process.stdout.readline()
        #     if len(output) == 0 and process.poll() is not None:
        #         break

        # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        # for line in proc.stdout:
        #     text_log.write(line)

        # cmd = ["sudo nmap", "-p- --min-rate-1000 -T4 127.0.0.1 | grep ^[0-9] | cut -d '/' -f 1 | 1 | tr '\n' ',' | sed)"]
        # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        # for line in proc.stdout:
        #     text_log.write(line)

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""

        # text_log = self.query_one(TextLog)

        # text_log.write("[bold magenta]Write text or any Rich renderable!")

    def run_command(command):
        """Start process for a cli command"""
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
        # text_log = self.query_one(TextLog)
        # process = subprocess.Popen(command, stdout=subprocess.PIPE)
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         text_log.write(output.strip())
        # rc = process.poll()
        # return rc

    def update_output(self) -> None:
        """Called on a set interval to update command output"""
        if self.running_scan:
            self.output = self.process.stdout.readline()

    def watch_output(self, output: str) -> None:
        """Called when the command output updates"""
        text_log = self.query_one(TextLog)
        text_log.write(output)
