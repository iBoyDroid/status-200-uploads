from typing import Literal

ListMediaFilesType = Literal["image", "video"]

LIST_MEDIA_FILES_TYPE_VALUES: set[ListMediaFilesType] = {
    "image",
    "video",
}


def check_list_media_files_type(value: str) -> ListMediaFilesType:
    if value in LIST_MEDIA_FILES_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_MEDIA_FILES_TYPE_VALUES!r}")
