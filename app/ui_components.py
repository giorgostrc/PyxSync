import math
import os
import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from tkinter.ttk import Progressbar
from typing import List, Union

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


class AddRemoveEntryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.add_path_button = tk.Button(self, text="Add source")
        self.add_path_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        self.remove_path_button = tk.Button(self, text="Remove source")
        self.remove_path_button.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))


class DirSelectionFrame(tk.Frame):
    def __init__(self, master, selector_type, width):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.selector_type = selector_type
        self.title = f"{self.selector_type} selector"
        self.width = width

        self.path_entry = tk.Entry(self, width=math.floor(0.8 * self.width))
        self.path_entry.insert(0, f"Select a path to file {self.selector_type} ...")
        self.path_entry.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="EW")

        self.browse_button = ButtonWithIcon(
            self,
            math.floor(0.1 * self.width),
            self.choose_directory,
            "",
            "icons/add_folder_icon_black.png",
            (24, 24),
        )
        self.browse_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

    def choose_directory(self):
        selected_dir = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, selected_dir)


class DirSelector(tk.Frame):
    def __init__(self, master, selector_type, width):
        super().__init__(master)
        self.selector_type = selector_type
        self.width = width
        self.entries = []
        self.create_path_entry(selector_type, width)

    def create_path_entry(self, selector_type, width, row=0):
        frame = DirSelectionFrame(self, selector_type, width)
        frame.grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")
        self.entries.append(frame)

    @property
    def text_entries(self) -> Union[str, List[str]]:
        if self.selector_type == "target":
            return self.entries[0].path_entry.get()

        return [entry.path_entry.get() for entry in self.entries]


class MultiDirSelector(DirSelector):
    def __init__(self, master, selector_type, width):
        super().__init__(master, selector_type, width)
        self.add_remove_entry_frame = AddRemoveEntryFrame(self)
        self.add_remove_entry_frame.add_path_button.config(command=self.add_path_entry)
        self.add_remove_entry_frame.remove_path_button.config(command=self.remove_path_entry)
        self.add_remove_entry_frame.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")

    def add_path_entry(self):
        num_existing = len(self.entries)
        self.add_remove_entry_frame.grid(row=1 + num_existing, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")
        self.create_path_entry(self.selector_type, self.width, num_existing)

    def remove_path_entry(self):
        num_existing = len(self.entries)
        if num_existing < 2:
            raise ValueError("Insufficient number of entries. Could not remove!")

        last_path_entry = self.entries.pop()
        self.add_remove_entry_frame.grid(row=num_existing, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")
        if last_path_entry:
            last_path_entry.destroy()


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
