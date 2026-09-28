from typing import Literal

YouTubeOptionsPrivacyStatus = Literal["private", "public", "unlisted"]

YOU_TUBE_OPTIONS_PRIVACY_STATUS_VALUES: set[YouTubeOptionsPrivacyStatus] = {
    "private",
    "public",
    "unlisted",
}


def check_you_tube_options_privacy_status(value: str) -> YouTubeOptionsPrivacyStatus:
    if value in YOU_TUBE_OPTIONS_PRIVACY_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {YOU_TUBE_OPTIONS_PRIVACY_STATUS_VALUES!r}"
    )
