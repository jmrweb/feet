from __future__ import annotations

import subprocess
from pathlib import Path

from textual import log

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Label, TextLog, Input

from feetmodule import FeetModule

print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

class Terminal(FeetModule):
    """Display a basic text box"""

    DEFAULT_CSS = """
    Terminal {
        width: 100%;
        height:100%;
        padding: 0 0;
        margin: 0 0 3 0;
        background: $panel;
        color: $text;
        border: $secondary solid;
        border_title_align: center;
        content-align: center middle;
    }

    #output_log {
        padding: 0 0;
        background: $panel;
        color: $text;
        /*border: $secondary solid;*/
        /*border_title_align: center;*/
        content-align: center middle;
    }
    
    #input_bar {
        dock: bottom;
        padding: 0 0;
        height: 1;
        width: 100%;
        
    }

    #input {
        padding: 0 0;
        height: 1;
        width: 1;
    }

    #input {
        padding: 0 0;
        height: 1;
        width: 100%;
        border: none;
    }
    """

    class CommandComplete(Message):
        "Message posted when the terminal output is updated."

        def __init__(self, terminal: Terminal) -> None:
            self.terminal = terminal
            super().__init__()


    class OutputUpdated(Message):
        "Message posted when the terminal output is updated."

        def __init__(self, terminal: Terminal) -> None:
            self.terminal = terminal
            super().__init__()


    def __init__(self, *args, title: str | None = None, interactive: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self._process = None
        self.output = ""
        self.text_log = None
        self.border_title = title
        self.interactive = interactive
        self.update_timer = self.set_interval(1/60, self._update_output, pause=True)

    def compose(self) -> ComposeResult:
        yield TextLog(id='output_log', highlight=True, markup=False)
        with Horizontal(id = 'input_bar'):
            yield Label('$ ', id='prompt')
            yield Input(id='input')


    def on_mount(self) -> None:
        """Called when the module is mounted to the app"""

        #Initialize TextLog
        self.text_log = self.query_one(TextLog)
        
        #Check interactive mode
        if not self.interactive:
            self.query_one('#input_bar').remove()
        
        #self.border_title = self.title
        #self.query_one('#output_log').border_title = 'Output Log'


    def run_command(self, cmd: str):
        """Start process for a cli command"""

        # Start output update timer
        self.update_timer.resume()

        # Execute command
        try:
            self._process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            #time.sleep(0.1)
        except FileNotFoundError as exc:
            self.text_log.write(exc)
            self.update_timer.pause()

    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Called when a button is pressed
        cmd = event.value.split(' ')
        self.run_command(cmd)
        self.query_one(Input).value = ""


    def _update_output(self) -> None:
        """Called on a set interval to update command output"""

        if len(self.output) == 0 and self._process.poll() is not None:
            self.text_log.write(" ")
            self.update_timer.pause()
            self._process.stdout.close()
            self._process.kill()
            self._process.wait()
            self.post_message(Terminal.CommandComplete(self))
        elif self._process.stdout:
            self.output = self._process.stdout.readline()
            log(f'Updating output: {self.output}')
            self.text_log.write(str(self.output)[2:-3])
            self.post_message(Terminal.OutputUpdated(self))
