from typing import Literal

YouTubeOptionsLicense = Literal["creativeCommon", "youtube"]

YOU_TUBE_OPTIONS_LICENSE_VALUES: set[YouTubeOptionsLicense] = {
    "creativeCommon",
    "youtube",
}


def check_you_tube_options_license(value: str) -> YouTubeOptionsLicense:
    if value in YOU_TUBE_OPTIONS_LICENSE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {YOU_TUBE_OPTIONS_LICENSE_VALUES!r}"
    )
