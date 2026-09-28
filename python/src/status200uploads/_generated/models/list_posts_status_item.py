from typing import Literal

ListPostsStatusItem = Literal[
    "cancelled", "failed", "processing", "scheduled", "success", "timeout"
]

LIST_POSTS_STATUS_ITEM_VALUES: set[ListPostsStatusItem] = {
    "cancelled",
    "failed",
    "processing",
    "scheduled",
    "success",
    "timeout",
}


def check_list_posts_status_item(value: str) -> ListPostsStatusItem:
    if value in LIST_POSTS_STATUS_ITEM_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_POSTS_STATUS_ITEM_VALUES!r}"
    )
