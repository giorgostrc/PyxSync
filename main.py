import os
import shutil
from datetime import datetime
from enum import Enum
from typing import List, Optional

import exifread
import psutil
from tqdm import tqdm


class ExtensionsEnum(Enum):
    @classmethod
    def to_list(cls):
        return list(map(lambda c: c.value, cls))


class ImageExtensions(ExtensionsEnum):
    JPG = ".JPG"
    JPEG = ".JPEG"


class RAWImageExtensions(ExtensionsEnum):
    ARW = ".ARW"
    NEF = ".NEF"


class VideoExtensions(ExtensionsEnum):
    MP4 = ".MP4"


def detect_removable_storage() -> List[str]:
    partitions = psutil.disk_partitions(all=True)
    external_storage_devices = [
        partition.device
        for partition in partitions
        if any(option in partition.opts for option in ["removable", "external"]) and "rw" in partition.opts
    ]
    return external_storage_devices


def detect_local_storage() -> List[str]:
    partitions = psutil.disk_partitions(all=True)
    local_storage_devices = [
        partition.device for partition in partitions if all(option in partition.opts for option in ["fixed", "rw"])
    ]
    return local_storage_devices


def select_device(storage_devices: List[str]) -> Optional[str]:
    if not storage_devices:
        print("No devices were found! Please connect an external storage!")

    print("External Devices:")
    for i, device in enumerate(storage_devices):
        print(f"{i}: {device}")

    try:
        selected_idx = int(input("Select a device id: "))
        if selected_idx <= len(storage_devices):
            selected_device = storage_devices[selected_idx]
            print(f"Selected device {selected_idx}: {selected_device}")
            return selected_device
    except Exception as e:
        print(f"Invalid input: {e}")

    return None


def find_images_videos(selected_device: str) -> Optional[List[str]]:
    # TODO: Add user option from_dcim_only: bool for image files
    all_extensions = ImageExtensions.to_list() + RAWImageExtensions.to_list() + VideoExtensions.to_list()
    detected_files = []

    print("Searching for files ...")
    for root, _, files in os.walk(selected_device):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.upper() in all_extensions:
                detected_files.append(os.path.join(root, file))

    if not detected_files:
        print("No files were found!")
        return []

    print(f"Found {len(detected_files)} files.")
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
            print(f"Warning: '{filepath}' is not a valid file path.")


def main():
    removable_storage_devices = detect_removable_storage()
    source_device = select_device(removable_storage_devices)
    source_files = find_images_videos(source_device)
    camera_model = get_camera_model(source_files[0])
    date_range = get_photo_date_range(source_files)
    local_storage_devices = detect_local_storage()
    target_device = select_device(local_storage_devices)
    target_dir = os.path.join(target_device, camera_model, date_range)
    print(f"Destination path: {target_dir}")
    copy_files(source_files, target_dir)


if __name__ == "__main__":
    main()
