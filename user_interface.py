import logging
import tkinter as tk
from tkinter import filedialog

logger = logging.getLogger()


class UserInterface:
    def __init__(self):
        self.ui = tk.Tk()
        self.ui.withdraw()

    def choose_directory(self) -> str:
        return filedialog.askdirectory()

    def display_message(self, message):
        window = tk.Toplevel(self.ui)
        window.title("PyxSync")
        window.geometry("+%d+%d" % (window.winfo_screenwidth() // 2 - 150, window.winfo_screenheight() // 2 - 50))
        logger.info(message)
        msg_label = tk.Label(window, text=message)
        msg_label.pack(pady=10)

        def proceed():
            logger.info("OK")
            window.destroy()

        next_button = tk.Button(window, text="Next", command=proceed)
        next_button.pack(pady=10)
        window.wait_window()
