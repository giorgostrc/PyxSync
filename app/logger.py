import logging
from tkinter import END

formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s --> %(message)s", "%Y-%m-%d %H:%M")


class UILogsHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox
        self.setFormatter(formatter)
        self.setLevel(logging.INFO)

    def emit(self, record):
        msg = self.format(record)
        self.textbox.configure(state="normal")
        self.textbox.insert(END, msg + "\n")
        self.textbox.configure(state="disabled")
        self.textbox.yview(END)


logger = logging.getLogger("PyxSync")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

logger.addHandler(console)
