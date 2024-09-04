import threading
import tkinter as tk

from app.logger import logger
from app.processing import run_process
from app.progress import ProgressTracker
from app.storage_manager import StorageManager
from app.ui_components import DirSelector, DisplayLogsFrame, MultiDirSelector, ProgressBar, TitleLabel


class PyxSyncUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PyxSync")
        width, height = (500, 440)
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.title_textbox = TitleLabel(self, "Welcome to PyxSync", 24)
        self.title_textbox.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.select_source_frame = MultiDirSelector(self, "source", width)
        self.select_source_frame.grid(row=1, column=0, padx=(10, 10), sticky="NSEW")

        self.select_target_frame = DirSelector(self, "target", width)
        self.select_target_frame.grid(row=2, column=0, padx=(10, 10), sticky="NSEW")

        self.start_progress_frame = tk.Frame(self)
        self.start_progress_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="NSEW")
        self.start_progress_frame.grid_columnconfigure(1, weight=10)

        self.transfer_files_btn = tk.Button(
            self.start_progress_frame, text="Start file transfer", command=self.start_process
        )
        self.transfer_files_btn.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="EW")

        self.progress_bar = ProgressBar(self.start_progress_frame, width)
        self.progress_bar.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="EW")

        self.logs_display = DisplayLogsFrame(self, width)
        self.logs_display.grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="NSEW")

    def start_process(self):
        self.transfer_files_btn.config(state=tk.DISABLED)
        self.progress_bar.reset_bar()
        try:
            storage = StorageManager(
                self.select_source_frame.text_entries,
                self.select_target_frame.text_entries,
            )
            prog_tracker = ProgressTracker(self.progress_bar)
            thread = threading.Thread(target=run_process, args=(storage, prog_tracker, self.transfer_files_btn))
            thread.start()
        except Exception as e:
            logger.error(f"Couldn't start process with error: {e}")
