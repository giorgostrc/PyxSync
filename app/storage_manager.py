import os.path
from typing import Set


class StorageManager:
    def __init__(self, sources: Set[str], target: str):
        if any(not isinstance(path, str) for path in sources):
            raise TypeError(f"Provided paths {sources} must be a str")
        if any(not os.path.exists(path) for path in sources):
            raise ValueError(f"Provided paths {sources} must exist")
        self._sources = sources

        if not isinstance(target, str):
            raise TypeError(f"Provided path {target} must be a str")
        self._target = target

    @property
    def sources(self):
        return self._sources

    @property
    def target(self):
        return self._target
