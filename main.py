import logging
import os

from processing import copy_files, find_images_videos, get_camera_model, get_photo_date_range
from storage_manager import StorageManager
from user_interface import UserInterface

logger = logging.getLogger()


def main():
    ui = UserInterface()
    ui.display_message("Welcome to PyxSync!")
    storage_manager = StorageManager()
    ui.display_message("Please select the source directory ...")
    storage_manager.source_storage = ui.choose_directory()
    source_files = find_images_videos(storage_manager.source_storage)
    camera_model = get_camera_model(source_files[0])
    date_range = get_photo_date_range(source_files)
    ui.display_message("Please select the target directory ...")
    storage_manager.target_storage = ui.choose_directory()
    target_dir = os.path.join(storage_manager.target_storage, camera_model, date_range)
    logger.info(f"Destination path: {target_dir}")
    copy_files(source_files, target_dir)


if __name__ == "__main__":
    main()
