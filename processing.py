import os
import shutil
from datetime import datetime
from enum import Enum
from typing import List, Optional

import exifread
from tqdm import tqdm

from file_extensions import ImageExtensions, RAWImageExtensions, VideoExtensions
from logger import logger
from storage_manager import StorageManager


class FileHandlingModes(Enum):
    RAW = "RAW"
    JPG = "JPG"
    IMG = "IMG"
    VID = "VID"


def find_files(selected_device: str, mode: FileHandlingModes) -> Optional[List[str]]:
    mode_target_files = {
        FileHandlingModes.RAW: RAWImageExtensions.to_list(),
        FileHandlingModes.JPG: ImageExtensions.to_list(),
        FileHandlingModes.IMG: ImageExtensions.to_list() + RAWImageExtensions.to_list(),
        FileHandlingModes.VID: VideoExtensions.to_list(),
    }
    target_extensions = mode_target_files[mode]
    detected_files = []

    logger.info(f"Searching for {target_extensions} files ...")
    for root, _, files in os.walk(selected_device):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.upper() in target_extensions:
                detected_files.append(os.path.join(root, file))

    if not detected_files:
        logger.info(f"No {target_extensions} files were found!")
        return []

    logger.info(f"Found {len(detected_files)} {target_extensions} files.")
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


def process_files(storage: StorageManager) -> None:
    raw_files = find_files(storage.source, FileHandlingModes.RAW)
    if not raw_files:
        logger.error(f"No RAW files were found in: {storage.source}")
        return

    camera_model = get_camera_model(raw_files[0])
    date_range = get_photo_date_range(raw_files)
    target_dir = os.path.join(storage.target, camera_model, date_range)
    logger.info(f"Destination path: {target_dir}")
    copy_files(raw_files, target_dir)

    jpg_files = find_files(storage.source, FileHandlingModes.JPG)
    if jpg_files:
        jpg_target_dir = os.path.join(target_dir, "JPG/")
        copy_files(jpg_files, jpg_target_dir)

    vid_files = find_files(storage.source, FileHandlingModes.VID)
    if vid_files:
        vid_target_dir = os.path.join(target_dir, "MOV/")
        copy_files(vid_files, vid_target_dir)
