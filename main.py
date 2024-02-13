import os
from enum import Enum

import psutil

# import exifread


def detect_storage():
    partitions = psutil.disk_partitions(all=True)
    external_storage_devices = [
        partition.device
        for partition in partitions
        if any(option in partition.opts for option in ["removable", "external"])
    ]
    return external_storage_devices


def select_device(external_storage_devices):
    if not external_storage_devices:
        print("No devices were found! Please connect an external storage!")

    print("External Devices:")
    for i, device in enumerate(external_storage_devices):
        print(f"{i}: {device}")

    try:
        selected_idx = int(input("Select a device id: "))
        if selected_idx <= len(external_storage_devices):
            selected_device = external_storage_devices[selected_idx]
            print(f"Selected device {selected_idx}: {selected_device}")
            return selected_device
    except Exception as e:
        print(f"Invalid input: {e}")


class ImageExtensions(Enum):
    JPG = ".JPG"
    JPEG = ".JPEG"

    @classmethod
    def to_list(cls):
        return list(map(lambda c: c.value, cls))


class RAWImageExtensions(Enum):
    ARW = ".ARW"
    NEF = ".NEF"

    @classmethod
    def to_list(cls):
        return list(map(lambda c: c.value, cls))


def find_images(selected_device):
    all_image_extensions = ImageExtensions.to_list() + RAWImageExtensions.to_list()
    image_files = []

    print("Searching for files ...")
    for root, _, files in os.walk(selected_device):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.upper() in all_image_extensions:
                image_files.append(os.path.join(root, file))

    if not image_files:
        print("No image files were found!")
        return []

    print(f"Found {len(image_files)} image files.")
    return image_files


def get_camera_model(image_paths):
    # extensions = RAWImageExtensions.to_list()
    # image_paths = [path for path in image_paths if os.path.splitext(path) in extensions]
    pass


def main():
    devices = detect_storage()
    selected_device = select_device(devices)
    if selected_device:
        image_files = find_images(selected_device)
        get_camera_model(image_files)


if __name__ == "__main__":
    main()
