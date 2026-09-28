from typing import Literal

Platform = Literal[
    "facebook", "instagram", "linkedin", "pinterest", "skool", "threads", "tiktok", "x", "youtube"
]

PLATFORM_VALUES: set[Platform] = {
    "facebook",
    "instagram",
    "linkedin",
    "pinterest",
    "skool",
    "threads",
    "tiktok",
    "x",
    "youtube",
}


def check_platform(value: str) -> Platform:
    if value in PLATFORM_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PLATFORM_VALUES!r}")
