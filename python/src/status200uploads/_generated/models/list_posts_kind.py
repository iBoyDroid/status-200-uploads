from typing import Literal

ListPostsKind = Literal["post", "scheduled_post"]

LIST_POSTS_KIND_VALUES: set[ListPostsKind] = {
    "post",
    "scheduled_post",
}


def check_list_posts_kind(value: str) -> ListPostsKind:
    if value in LIST_POSTS_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_POSTS_KIND_VALUES!r}")
