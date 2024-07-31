import math
import os
import threading
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image

from logger import UILogsHandler, logger
from processing import run_process
from progress import ProgressTracker
from storage_manager import StorageManager

basedir = os.path.dirname(__file__)


class PyxSyncUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyxSync")
        width, height = (500, 440)
        self.geometry(f"{width}x{height}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.title_textbox = TitleLabel(self, "Welcome to PyxSync", 24)
        self.title_textbox.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.select_source_frame = DirSelectionFrame(self, "source", width)
        self.select_source_frame.grid(row=1, column=0, padx=(10, 10), sticky="NSEW")

        self.select_target_frame = DirSelectionFrame(self, "target", width)
        self.select_target_frame.grid(row=2, column=0, padx=(10, 10), sticky="NSEW")

        self.transfer_files_btn = ctk.CTkButton(self, text="Start file transfer", command=self.start_process)
        self.transfer_files_btn.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))

        self.progress_bar = ProgressBar(self, width)
        self.progress_bar.grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="EW")

        self.logs_display = DisplayLogsFrame(self, width)
        self.logs_display.grid(row=5, column=0, padx=(10, 10), pady=(10, 10), sticky="NSEW")

    def start_process(self):
        self.transfer_files_btn.configure(state=ctk.DISABLED)
        self.progress_bar.reset_bar()
        try:
            storage = StorageManager(
                self.select_source_frame.path_entry.get(),
                self.select_target_frame.path_entry.get(),
            )
            prog_tracker = ProgressTracker(self.progress_bar)
            thread = threading.Thread(target=run_process, args=(storage, prog_tracker, self.transfer_files_btn))
            thread.start()
        except Exception as e:
            logger.error(f"Couldn't start process with error: {e}")


class TitleLabel(ctk.CTkLabel):
    def __init__(self, master, text, font_size):
        super().__init__(master, text=text, font=ctk.CTkFont(size=font_size))
        self.anchor = "center"


class ButtonWithIcon(ctk.CTkButton):
    def __init__(self, master, width, command, text, icon_path, icon_size):
        icon_path = os.path.join(basedir, icon_path)
        icon = ctk.CTkImage(Image.open(icon_path), size=icon_size)
        super().__init__(master, width=width, command=command, text=text, image=icon)


class DirSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, selector_type, width):
        super().__init__(master)
        self.title = f"{selector_type} selector"
        self.grid_columnconfigure(1, weight=1)

        self.browse_button = ButtonWithIcon(
            self,
            math.floor(0.1 * width),
            self.choose_directory,
            "",
            "icons/add_folder_icon.png",
            (24, 24),
        )
        self.browse_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.path_entry = ctk.CTkEntry(
            self, placeholder_text=f"Select a path to file {selector_type} ...", width=math.floor(0.8 * width)
        )
        self.path_entry.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="EW")

    def choose_directory(self):
        selected_dir = filedialog.askdirectory()
        self.path_entry.delete(0, ctk.END)
        self.path_entry.insert(0, selected_dir)


class DisplayLogsFrame(ctk.CTkFrame):
    def __init__(self, master, width):
        super().__init__(master)
        self.title = "logs display"
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.logs_box = ctk.CTkTextbox(self, activate_scrollbars=False)
        self.logs_box.grid(row=0, column=0, sticky="nsew")
        self.logs_box.configure(state="disabled")

        ctk_textbox_scrollbar = ctk.CTkScrollbar(self, command=self.logs_box.yview)
        ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")
        self.logs_box.configure(yscrollcommand=ctk_textbox_scrollbar.set)

        logs_handler = UILogsHandler(self.logs_box)
        logger.addHandler(logs_handler)


class ProgressBar(ctk.CTkProgressBar):
    def __init__(self, master, width):
        super().__init__(master, width=math.floor(0.8 * width))
        self.reset_bar()

    def reset_bar(self):
        self.set(0)
        self.configure(progress_color="blue")

    def set_success(self):
        self.set(1)
        self.configure(progress_color="green")
