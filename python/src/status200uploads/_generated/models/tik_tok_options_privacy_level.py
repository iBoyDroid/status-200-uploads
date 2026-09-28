from typing import Literal

TikTokOptionsPrivacyLevel = Literal[
    "FOLLOWER_OF_CREATOR", "MUTUAL_FOLLOW_FRIENDS", "PUBLIC_TO_EVERYONE", "SELF_ONLY"
]

TIK_TOK_OPTIONS_PRIVACY_LEVEL_VALUES: set[TikTokOptionsPrivacyLevel] = {
    "FOLLOWER_OF_CREATOR",
    "MUTUAL_FOLLOW_FRIENDS",
    "PUBLIC_TO_EVERYONE",
    "SELF_ONLY",
}


def check_tik_tok_options_privacy_level(value: str) -> TikTokOptionsPrivacyLevel:
    if value in TIK_TOK_OPTIONS_PRIVACY_LEVEL_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TIK_TOK_OPTIONS_PRIVACY_LEVEL_VALUES!r}"
    )
