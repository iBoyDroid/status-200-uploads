from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TikTokPostingOptions")


@_attrs_define
class TikTokPostingOptions:
    """
    Attributes:
        privacy_level_options (list[str] | Unset): The only values TikTok will accept in post.tiktok.privacyLevel for
            this account (empty = it will not take a post right now).
        comment_disabled (bool | Unset):
        duet_disabled (bool | Unset):
        stitch_disabled (bool | Unset):
        max_video_post_duration_sec (float | None | Unset):
        creator_username (None | str | Unset):
        creator_nickname (None | str | Unset):
    """

    privacy_level_options: list[str] | Unset = UNSET
    comment_disabled: bool | Unset = UNSET
    duet_disabled: bool | Unset = UNSET
    stitch_disabled: bool | Unset = UNSET
    max_video_post_duration_sec: float | None | Unset = UNSET
    creator_username: None | str | Unset = UNSET
    creator_nickname: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        privacy_level_options: list[str] | Unset = UNSET
        if not isinstance(self.privacy_level_options, Unset):
            privacy_level_options = self.privacy_level_options

        comment_disabled = self.comment_disabled

        duet_disabled = self.duet_disabled

        stitch_disabled = self.stitch_disabled

        max_video_post_duration_sec: float | None | Unset
        if isinstance(self.max_video_post_duration_sec, Unset):
            max_video_post_duration_sec = UNSET
        else:
            max_video_post_duration_sec = self.max_video_post_duration_sec

        creator_username: None | str | Unset
        if isinstance(self.creator_username, Unset):
            creator_username = UNSET
        else:
            creator_username = self.creator_username

        creator_nickname: None | str | Unset
        if isinstance(self.creator_nickname, Unset):
            creator_nickname = UNSET
        else:
            creator_nickname = self.creator_nickname

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if privacy_level_options is not UNSET:
            field_dict["privacy_level_options"] = privacy_level_options
        if comment_disabled is not UNSET:
            field_dict["comment_disabled"] = comment_disabled
        if duet_disabled is not UNSET:
            field_dict["duet_disabled"] = duet_disabled
        if stitch_disabled is not UNSET:
            field_dict["stitch_disabled"] = stitch_disabled
        if max_video_post_duration_sec is not UNSET:
            field_dict["max_video_post_duration_sec"] = max_video_post_duration_sec
        if creator_username is not UNSET:
            field_dict["creator_username"] = creator_username
        if creator_nickname is not UNSET:
            field_dict["creator_nickname"] = creator_nickname

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        privacy_level_options = cast(list[str], d.pop("privacy_level_options", UNSET))

        comment_disabled = d.pop("comment_disabled", UNSET)

        duet_disabled = d.pop("duet_disabled", UNSET)

        stitch_disabled = d.pop("stitch_disabled", UNSET)

        def _parse_max_video_post_duration_sec(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_video_post_duration_sec = _parse_max_video_post_duration_sec(
            d.pop("max_video_post_duration_sec", UNSET)
        )

        def _parse_creator_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        creator_username = _parse_creator_username(d.pop("creator_username", UNSET))

        def _parse_creator_nickname(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        creator_nickname = _parse_creator_nickname(d.pop("creator_nickname", UNSET))

        tik_tok_posting_options = cls(
            privacy_level_options=privacy_level_options,
            comment_disabled=comment_disabled,
            duet_disabled=duet_disabled,
            stitch_disabled=stitch_disabled,
            max_video_post_duration_sec=max_video_post_duration_sec,
            creator_username=creator_username,
            creator_nickname=creator_nickname,
        )

        tik_tok_posting_options.additional_properties = d
        return tik_tok_posting_options

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
