from typing import Literal

PostItemKind = Literal["post"]

POST_ITEM_KIND_VALUES: set[PostItemKind] = {
    "post",
}


def check_post_item_kind(value: str) -> PostItemKind:
    if value in POST_ITEM_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {POST_ITEM_KIND_VALUES!r}")
