import math
from tkinter import END, filedialog

import customtkinter as ctk

from processing import process_files
from storage_manager import StorageManager


class PyxSyncUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyxSync")
        width, height = (500, 320)
        self.geometry(f"{width}x{height}")
        self.grid_columnconfigure(0, weight=1)

        self.title_textbox = TitleLabel(self, "Welcome to PyxSync", 24)
        self.title_textbox.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.select_source_frame = DirSelectionFrame(self, "source", width)
        self.select_source_frame.grid(row=1, column=0, padx=(10, 10))

        self.select_target_frame = DirSelectionFrame(self, "target", width)
        self.select_target_frame.grid(row=2, column=0, padx=(10, 10))

        self.transfer_files_btn = ctk.CTkButton(self, text="Start file transfer", command=self.run_process)
        self.transfer_files_btn.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))

    def run_process(self):
        storage_manager = StorageManager()
        storage_manager.source_storage = self.select_source_frame.path_entry.get()
        storage_manager.target_storage = self.select_target_frame.path_entry.get()
        process_files(storage_manager.source_storage, storage_manager.target_storage)


class TitleLabel(ctk.CTkLabel):
    def __init__(self, master, text, font_size):
        super().__init__(master, text=text, font=ctk.CTkFont(size=font_size))
        self.anchor = "center"


class DirSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, type, width):
        super().__init__(master)
        self.title = f"{type} selector"
        self.grid_columnconfigure(1, weight=1)

        self.browse_button = ctk.CTkButton(
            self, text="Browse ...", width=math.floor(0.2 * width), command=self.choose_directory
        )
        self.browse_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.path_entry = ctk.CTkEntry(
            self, placeholder_text=f"Filepath to image/video file {type} ...", width=math.floor(0.7 * width)
        )
        self.path_entry.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

    def choose_directory(self):
        selected_dir = filedialog.askdirectory()
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, selected_dir)
