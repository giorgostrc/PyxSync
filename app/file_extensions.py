from enum import Enum


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
