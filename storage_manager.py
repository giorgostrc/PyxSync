import os.path
from typing import Optional


class StorageManager:
    def __init__(self, source_storage: Optional[str] = None, target_storage: Optional[str] = None):
        self._source_storage = source_storage
        self._target_storage = target_storage

    @property
    def source_storage(self):
        return self._source_storage

    @source_storage.setter
    def source_storage(self, new_source):
        if not isinstance(new_source, str):
            raise TypeError(f"Provided path {new_source} must be a str")
        if not os.path.exists(new_source):
            raise ValueError(f"Provided path {new_source} does not exist")
        self._source_storage = new_source

    @property
    def target_storage(self):
        return self._target_storage

    @target_storage.setter
    def target_storage(self, new_target):
        if not isinstance(new_target, str):
            raise TypeError(f"Provided path {new_target} must be a str")
        if not os.path.exists(new_target):
            raise ValueError(f"Provided path {new_target} does not exist")
        self._target_storage = new_target
