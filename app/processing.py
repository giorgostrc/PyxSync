import os
import shutil
from datetime import datetime
from enum import Enum
from typing import List

import customtkinter as ctk
import exifread
from tqdm import tqdm

from app.file_extensions import ImageExtensions, RAWImageExtensions, VideoExtensions
from app.logger import logger
from app.progress import ProgressTracker
from app.storage_manager import StorageManager


class FileHandlingModes(Enum):
    RAW = "RAW"
    JPG = "JPG"
    IMG = "IMG"
    VID = "VID"


def find_files(selected_device: str, mode: FileHandlingModes) -> List[str]:
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


def copy_files(filepaths: List[str], target_dir: str, prog_tracker: ProgressTracker) -> None:
    os.makedirs(target_dir, exist_ok=False)
    for i, filepath in tqdm(enumerate(filepaths), desc="Copying over files ... ", total=len(filepaths)):
        prog_tracker.report_progress(1)
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            destination = os.path.join(target_dir, filename)
            shutil.copy2(filepath, destination)
        else:
            logger.warning(f"{filepath} is not a valid file path.")


def process_files(storage: StorageManager, prog_tracker: ProgressTracker) -> None:
    raw_files = []
    jpg_files = []
    vid_files = []
    for source in storage.sources:
        logger.info(f"Scanning source dir: {source}")
        raw_files.extend(find_files(source, FileHandlingModes.RAW))
        jpg_files.extend(find_files(source, FileHandlingModes.JPG))
        vid_files.extend(find_files(source, FileHandlingModes.VID))

    if not raw_files:
        logger.error(f"No RAW files were found in: {storage.sources}")
        return

    prog_tracker.add_total_steps(len(raw_files) + len(jpg_files) + len(vid_files))

    camera_model = get_camera_model(raw_files[0])
    date_range = get_photo_date_range(raw_files)
    target_dir = os.path.join(storage.target, camera_model, date_range)
    logger.info(f"Destination path: {target_dir}")
    copy_files(raw_files, target_dir, prog_tracker)

    if jpg_files:
        jpg_target_dir = os.path.join(target_dir, "JPG/")
        copy_files(jpg_files, jpg_target_dir, prog_tracker)

    if vid_files:
        vid_target_dir = os.path.join(target_dir, "MOV/")
        copy_files(vid_files, vid_target_dir, prog_tracker)


def run_process(storage: StorageManager, prog_tracker: ProgressTracker, start_process_btn: ctk.CTkButton) -> None:
    try:
        process_files(storage, prog_tracker)
    except Exception as e:
        logger.error(f"Couldn't complete file transfer with error: {e}")
    finally:
        start_process_btn.configure(state=ctk.NORMAL)
