import os.path
from typing import Optional


class StorageManager:
    def __init__(self, source: Optional[str] = None, target: Optional[str] = None):
        self._source = source
        self._target = target

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, new_source):
        if not isinstance(new_source, str):
            raise TypeError(f"Provided path {new_source} must be a str")
        if not os.path.exists(new_source):
            raise ValueError(f"Provided path {new_source} does not exist")
        self._source = new_source

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, new_target):
        if not isinstance(new_target, str):
            raise TypeError(f"Provided path {new_target} must be a str")
        if not os.path.exists(new_target):
            raise ValueError(f"Provided path {new_target} does not exist")
        self._target = new_target
