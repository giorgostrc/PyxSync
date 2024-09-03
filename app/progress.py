from typing import Optional

from app.logger import logger
from app.ui_components import ProgressBar


class ProgressTracker:
    def __init__(self, progress_bar: Optional[ProgressBar] = None):
        self._total_steps = 0
        self._completed_steps = 0
        self._progress_bar = progress_bar

    def set_total_steps(self, steps: int) -> None:
        self._total_steps = steps

    def add_total_steps(self, steps: int) -> None:
        self._total_steps += steps

    def report_progress(self, steps: int) -> None:
        self._completed_steps += steps
        self.update_progress()

    def update_progress(self) -> None:
        if not self._progress_bar:
            return

        if self._total_steps == 0 or self._total_steps < self._completed_steps:
            logger.warning("Unable to update progress bar")
            return

        progress = self._completed_steps / self._total_steps
        self._progress_bar["value"] = progress

    @property
    def progress_bar(self):
        return self._progress_bar
