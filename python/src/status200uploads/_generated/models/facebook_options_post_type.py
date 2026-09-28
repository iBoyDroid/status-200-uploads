from typing import Literal

FacebookOptionsPostType = Literal["photo", "reel", "text", "video"]

FACEBOOK_OPTIONS_POST_TYPE_VALUES: set[FacebookOptionsPostType] = {
    "photo",
    "reel",
    "text",
    "video",
}


def check_facebook_options_post_type(value: str) -> FacebookOptionsPostType:
    if value in FACEBOOK_OPTIONS_POST_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FACEBOOK_OPTIONS_POST_TYPE_VALUES!r}"
    )
