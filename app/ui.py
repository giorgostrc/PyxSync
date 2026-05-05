import threading
import tkinter as tk
import tkinter.ttk as ttk

from app.logger import logger
from app.processing import run_process
from app.progress import ProgressTracker
from app.storage_manager import StorageManager
from app.ui_components import (
    DirSelector,
    DisplayLogsFrame,
    MultiDirSelector,
    ProgressBar,
    TitleLabel,
)

BG, FG, ACCENT = "#F7F7F8", "#1A1A1A", "#2563EB"


class PyxSyncUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self._setup_theme()

        self.title("PyxSync")
        width, height = (580, 540)
        self.geometry(f"{width}x{height}")
        self.minsize(500, 460)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self.title_textbox = TitleLabel(self, "Welcome to PyxSync", 24)
        self.title_textbox.grid(row=0, column=0, padx=10, pady=(10, 10))

        tk.Label(
            self, text="Source Directories", font=("Segoe UI", 9), fg="#6B7280"
        ).grid(row=1, column=0, padx=14, pady=(8, 0), sticky="W")

        self.select_source_frame = MultiDirSelector(self, "source")
        self.select_source_frame.grid(row=2, column=0, padx=10, sticky="NSEW")

        tk.Label(
            self, text="Target Directory", font=("Segoe UI", 9), fg="#6B7280"
        ).grid(row=3, column=0, padx=14, pady=(8, 0), sticky="W")

        self.select_target_frame = DirSelector(self, "target")
        self.select_target_frame.grid(row=4, column=0, padx=10, sticky="NSEW")

        self.transfer_files_btn = tk.Button(
            self,
            text="Start file transfer",
            command=self.start_process,
            bg=ACCENT,
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        )
        self.transfer_files_btn.grid(
            row=5, column=0, padx=14, pady=(12, 4), sticky="EW"
        )

        self.progress_bar = ProgressBar(self)
        self.progress_bar.grid(row=6, column=0, padx=14, pady=(0, 4), sticky="EW")

        self.logs_display = DisplayLogsFrame(self)
        self.logs_display.grid(row=7, column=0, padx=10, pady=(4, 10), sticky="NSEW")

    def _setup_theme(self):
        self.configure(bg=BG)
        self.option_add("*Background", BG)
        self.option_add("*Foreground", FG)
        self.option_add("*Font", "Segoe\\ UI 10")
        self.option_add("*Entry.Background", "#FFFFFF")
        self.option_add("*Text.Background", "#FFFFFF")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TProgressbar", troughcolor="#E5E7EB", background=ACCENT, thickness=8
        )

    def start_process(self):
        self.transfer_files_btn.config(state=tk.DISABLED, text="Transferring...")
        self.progress_bar.reset_bar()
        try:
            storage = StorageManager(
                self.select_source_frame.text_entries,
                self.select_target_frame.text_entries,
            )
            prog_tracker = ProgressTracker(self.progress_bar)
            thread = threading.Thread(
                target=run_process,
                args=(storage, prog_tracker, self.transfer_files_btn),
            )
            thread.start()
        except Exception as e:
            logger.error(f"Couldn't start process with error: {e}")
