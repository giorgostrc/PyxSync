from typing import List, Optional

import psutil


class StorageManager:
    def __init__(self):
        self.source_storage = None
        self.target_storage = None

    def detect_removable_storage(self) -> List[str]:
        try:
            partitions = psutil.disk_partitions(all=True)
            external_storage_devices = [
                partition.device
                for partition in partitions
                if any(option in partition.opts for option in ["removable", "external"]) and "rw" in partition.opts
            ]
            return external_storage_devices
        except Exception as e:
            raise RuntimeError(f"Error detecting removable storages: {e}")

    def detect_local_storage(self) -> List[str]:
        try:
            partitions = psutil.disk_partitions(all=True)
            local_storage_devices = [
                partition.device
                for partition in partitions
                if all(option in partition.opts for option in ["fixed", "rw"])
            ]
            return local_storage_devices
        except Exception as e:
            raise RuntimeError(f"Error detecting local storages: {e}")

    def select_device(self, storage_devices: List[str]) -> Optional[str]:
        if not storage_devices:
            raise ValueError("No devices were found! Please connect an external storage!")

        print("External Devices:")
        for i, device in enumerate(storage_devices):
            print(f"{i}: {device}")

        try:
            selected_idx = int(input("Select a device id: "))
            if 0 <= selected_idx <= len(storage_devices):
                selected_device = storage_devices[selected_idx]
                print(f"Selected device {selected_idx}: {selected_device}")
                return selected_device
            else:
                raise ValueError("Invalid device index selected.")
        except Exception as e:
            print(f"Error selecting device: {e}")

        return None

    def select_source_storage(self):
        removable_devices = self.detect_removable_storage()
        self.source_storage = self.select_device(removable_devices)

    def select_target_storage(self):
        local_devices = self.detect_local_storage()
        self.target_storage = self.select_device(local_devices)
