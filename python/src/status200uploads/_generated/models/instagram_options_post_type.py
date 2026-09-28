from typing import Literal

InstagramOptionsPostType = Literal["carousel", "feed_image", "reel", "story"]

INSTAGRAM_OPTIONS_POST_TYPE_VALUES: set[InstagramOptionsPostType] = {
    "carousel",
    "feed_image",
    "reel",
    "story",
}


def check_instagram_options_post_type(value: str) -> InstagramOptionsPostType:
    if value in INSTAGRAM_OPTIONS_POST_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INSTAGRAM_OPTIONS_POST_TYPE_VALUES!r}"
    )
