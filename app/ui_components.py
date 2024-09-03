import math
import os
import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk

from app.logger import UILogsHandler, logger

basedir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(basedir, os.pardir))


class TitleLabel(tk.Label):
    def __init__(self, master, text, font_size):
        font = Font(size=font_size)
        super().__init__(master, text=text, font=font)
        self.anchor = "center"


class ButtonWithIcon(tk.Button):
    def __init__(self, master, width, command, text, icon_path, icon_size):
        icon_path = os.path.join(root_path, icon_path)
        image = Image.open(icon_path)
        image = image.resize(icon_size, Image.Resampling.LANCZOS)
        self.icon = ImageTk.PhotoImage(image)
        super().__init__(master, width=width, command=command, text=text, image=self.icon, compound="left")


class DirSelectionFrame(tk.Frame):
    def __init__(self, master, selector_type, width):
        super().__init__(master)
        self.title = f"{selector_type} selector"
        self.grid_columnconfigure(1, weight=1)

        self.browse_button = ButtonWithIcon(
            self,
            math.floor(0.1 * width),
            self.choose_directory,
            "",
            "icons/add_folder_icon_black.png",
            (24, 24),
        )
        self.browse_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.path_entry = tk.Entry(self, width=math.floor(0.8 * width))
        self.path_entry.insert(0, f"Select a path to file {selector_type} ...")
        self.path_entry.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="EW")

    def choose_directory(self):
        selected_dir = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, selected_dir)


class DisplayLogsFrame(tk.Frame):
    def __init__(self, master, width):
        super().__init__(master)
        self.title = "logs display"
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.logs_box = tk.Text(self, state=tk.DISABLED, wrap="word")
        self.logs_box.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self, command=self.logs_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.logs_box.config(yscrollcommand=scrollbar.set)

        logs_handler = UILogsHandler(self.logs_box)
        logger.addHandler(logs_handler)


class ProgressBar(Progressbar):
    def __init__(self, master, width):
        super().__init__(master, length=math.floor(0.8 * width), mode="determinate")
        self.reset_bar()

    def reset_bar(self):
        self["value"] = 0

    def set_success(self):
        self["value"] = 100
