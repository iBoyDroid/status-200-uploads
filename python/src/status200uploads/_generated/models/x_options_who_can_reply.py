from typing import Literal

XOptionsWhoCanReply = Literal["everyone", "following", "mentionedUsers", "subscribers", "verified"]

X_OPTIONS_WHO_CAN_REPLY_VALUES: set[XOptionsWhoCanReply] = {
    "everyone",
    "following",
    "mentionedUsers",
    "subscribers",
    "verified",
}


def check_x_options_who_can_reply(value: str) -> XOptionsWhoCanReply:
    if value in X_OPTIONS_WHO_CAN_REPLY_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {X_OPTIONS_WHO_CAN_REPLY_VALUES!r}"
    )
