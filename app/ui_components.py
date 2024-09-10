import math
import os
import tkinter as tk
from functools import partial
from tkinter import filedialog
from tkinter.font import Font
from tkinter.ttk import Progressbar
from typing import Set, Union

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
        self.add_path_button = ButtonWithIcon(
            self,
            24,
            "",
            "",
            "icons/add.png",
            (24, 24),
        )
        self.add_path_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))


class DirSelectionFrame(tk.Frame):
    def __init__(self, master, selector_type, width):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.selector_type = selector_type
        self.title = f"{self.selector_type} selector"
        self.width = width

        self.path_entry = tk.Entry(self)
        self.path_entry.insert(0, f"Select a path to file {self.selector_type} ...")
        self.path_entry.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="EW")

        self.browse_button = ButtonWithIcon(
            self,
            24,
            self.choose_directory,
            "",
            "icons/browse.png",
            (24, 24),
        )
        self.browse_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="W")

        if selector_type == "source":
            self.remove_button = ButtonWithIcon(
                self,
                24,
                "",
                "",
                "icons/trash.png",
                (24, 24),
            )
            self.remove_button.grid(row=0, column=2, padx=(5, 5), pady=(5, 5), sticky="E")

    def choose_directory(self):
        selected_dir = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, selected_dir)


class DirSelector(tk.Frame):
    def __init__(self, master, selector_type, width):
        super().__init__(master)
        self.columnconfigure(0, weight=1)

        self.selector_type = selector_type
        self.width = width
        self.entries = []
        self.create_path_entry(selector_type, width)

    def create_path_entry(self, selector_type, width, row=0):
        frame = DirSelectionFrame(self, selector_type, width)
        if selector_type == "source":
            frame.remove_button.configure(command=partial(self.remove_entry, frame))

        frame.grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")
        self.entries.append(frame)

    @property
    def text_entries(self) -> Union[str, Set[str]]:
        if self.selector_type == "target":
            return self.entries[0].path_entry.get()

        return set([entry.path_entry.get() for entry in self.entries])

    def remove_entry(self, entry_frame):
        raise NotImplementedError("Can't remove entry in single path selector.")


class MultiDirSelector(DirSelector):
    def __init__(self, master, selector_type, width):
        super().__init__(master, selector_type, width)
        self.add_remove_entry_frame = AddRemoveEntryFrame(self)
        self.add_remove_entry_frame.add_path_button.config(command=self.add_path_entry)
        self.add_remove_entry_frame.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")

    def add_path_entry(self):
        num_existing = len(self.entries)
        self.add_remove_entry_frame.grid_forget()
        self.add_remove_entry_frame.grid(row=1 + num_existing, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")
        self.create_path_entry(self.selector_type, self.width, num_existing)

    def remove_entry(self, entry_frame):
        if len(self.entries) < 2:
            return

        self.entries.remove(entry_frame)
        entry_frame.destroy()

        num_existing = len(self.entries)
        for i, entry in enumerate(self.entries):
            entry.grid_forget()
            entry.grid(row=i, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")

        self.add_remove_entry_frame.grid_forget()
        self.add_remove_entry_frame.grid(row=num_existing, column=0, padx=(5, 5), pady=(5, 5), sticky="NSEW")


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
