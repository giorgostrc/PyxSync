import logging
import os
import shutil
from datetime import datetime
from typing import List, Optional

import exifread
from tqdm import tqdm

from file_extensions import ImageExtensions, RAWImageExtensions, VideoExtensions
from storage_manager import StorageManager
from user_interface import UserInterface

logger = logging.getLogger()


def find_images_videos(selected_device: str) -> Optional[List[str]]:
    all_extensions = ImageExtensions.to_list() + RAWImageExtensions.to_list() + VideoExtensions.to_list()
    detected_files = []

    logger.info("Searching for files ...")
    for root, _, files in os.walk(selected_device):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.upper() in all_extensions:
                detected_files.append(os.path.join(root, file))

    if not detected_files:
        logger.info("No files were found!")
        return []

    logger.info(f"Found {len(detected_files)} files.")
    return detected_files


def get_camera_model(filepath: str) -> str:
    f = open(filepath, "rb")
    tags = exifread.process_file(f)
    make = tags.get("Image Make")
    make = make.values.split(" ")[0]
    model = tags.get("Image Model")
    model = model.values
    if make in model:
        return model
    model = model.replace(make, "").strip(" ")
    return f"{make} {model}"


def get_photo_date_range(filepaths: List[str]) -> str:
    dates = []
    for filepath in filepaths:
        f = open(filepath, "rb")
        tags = exifread.process_file(f)
        date_shot = tags.get("Image DateTime")
        if date_shot:
            date_shot = date_shot.values.split(" ")[0]
            date_shot = datetime.strptime(date_shot, "%Y:%m:%d")
            dates.append(date_shot)
    dates = list(set(dates))
    if len(dates) == 1:
        return dates[0].strftime("%Y-%m-%d")
    earliest_date = min(dates).strftime("%Y-%m-%d")
    latest_date = max(dates).strftime("%Y-%m-%d")
    return f"{earliest_date} - {latest_date}"


def copy_files(filepaths: List[str], target_dir: str) -> None:
    os.makedirs(target_dir, exist_ok=False)
    for i, filepath in tqdm(enumerate(filepaths), desc="Copying over files ... ", total=len(filepaths)):
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            destination = os.path.join(target_dir, filename)
            shutil.copy2(filepath, destination)
        else:
            logger.warning(f"{filepath} is not a valid file path.")


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
