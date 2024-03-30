import logging

from processing import FileHandlingModes, process_files
from storage_manager import StorageManager
from user_interface import UserInterface

logger = logging.getLogger(__name__)


def main():
    ui = UserInterface()
    ui.display_message("Welcome to PyxSync!")

    storage_manager = StorageManager()
    ui.display_message("Please select the source directory ...")
    storage_manager.source_storage = ui.choose_directory()
    ui.display_message("Please select the target directory ...")
    storage_manager.target_storage = ui.choose_directory()
    process_files(storage_manager.source_storage, storage_manager.target_storage, FileHandlingModes.RAW)


if __name__ == "__main__":
    main()
