from typing import Literal

ScheduledPostItemKind = Literal["scheduled_post"]

SCHEDULED_POST_ITEM_KIND_VALUES: set[ScheduledPostItemKind] = {
    "scheduled_post",
}


def check_scheduled_post_item_kind(value: str) -> ScheduledPostItemKind:
    if value in SCHEDULED_POST_ITEM_KIND_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SCHEDULED_POST_ITEM_KIND_VALUES!r}"
    )
