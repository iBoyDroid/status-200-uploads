from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tik_tok_options_privacy_level import (
    TikTokOptionsPrivacyLevel,
    check_tik_tok_options_privacy_level,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TikTokOptions")


@_attrs_define
class TikTokOptions:
    """
    Attributes:
        privacy_level (TikTokOptionsPrivacyLevel | Unset): Only the levels GET /accounts/{profile_id}/options lists for
            the account are accepted by TikTok. privacyStatus (YouTube's name) is not read here: the post goes out as
            SELF_ONLY and warnings says so. Default: 'SELF_ONLY'.
        disabled_comments (bool | Unset):  Default: False.
        disabled_duet (bool | Unset): Videos only. Default: False.
        disabled_stitch (bool | Unset): Videos only. Default: False.
        is_branded_content (bool | Unset):  Default: False.
        is_your_brand (bool | Unset):  Default: False.
        is_ai_generated (bool | Unset): Videos only. Default: False.
        auto_add_music (bool | Unset): Photo posts only. Default: False.
        title (str | Unset): A photo post's title (up to 90 characters; longer is shortened at the end of a word). On a
            video it is the caption (up to 2,200 characters) instead of content.text.
        description (str | Unset): A photo post's description (up to 4,000 characters). Not used on a video.
    """

    privacy_level: TikTokOptionsPrivacyLevel | Unset = "SELF_ONLY"
    disabled_comments: bool | Unset = False
    disabled_duet: bool | Unset = False
    disabled_stitch: bool | Unset = False
    is_branded_content: bool | Unset = False
    is_your_brand: bool | Unset = False
    is_ai_generated: bool | Unset = False
    auto_add_music: bool | Unset = False
    title: str | Unset = UNSET
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        privacy_level: str | Unset = UNSET
        if not isinstance(self.privacy_level, Unset):
            privacy_level = self.privacy_level

        disabled_comments = self.disabled_comments

        disabled_duet = self.disabled_duet

        disabled_stitch = self.disabled_stitch

        is_branded_content = self.is_branded_content

        is_your_brand = self.is_your_brand

        is_ai_generated = self.is_ai_generated

        auto_add_music = self.auto_add_music

        title = self.title

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if privacy_level is not UNSET:
            field_dict["privacyLevel"] = privacy_level
        if disabled_comments is not UNSET:
            field_dict["disabledComments"] = disabled_comments
        if disabled_duet is not UNSET:
            field_dict["disabledDuet"] = disabled_duet
        if disabled_stitch is not UNSET:
            field_dict["disabledStitch"] = disabled_stitch
        if is_branded_content is not UNSET:
            field_dict["isBrandedContent"] = is_branded_content
        if is_your_brand is not UNSET:
            field_dict["isYourBrand"] = is_your_brand
        if is_ai_generated is not UNSET:
            field_dict["isAiGenerated"] = is_ai_generated
        if auto_add_music is not UNSET:
            field_dict["autoAddMusic"] = auto_add_music
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _privacy_level = d.pop("privacyLevel", UNSET)
        privacy_level: TikTokOptionsPrivacyLevel | Unset
        if isinstance(_privacy_level, Unset):
            privacy_level = UNSET
        else:
            privacy_level = check_tik_tok_options_privacy_level(_privacy_level)

        disabled_comments = d.pop("disabledComments", UNSET)

        disabled_duet = d.pop("disabledDuet", UNSET)

        disabled_stitch = d.pop("disabledStitch", UNSET)

        is_branded_content = d.pop("isBrandedContent", UNSET)

        is_your_brand = d.pop("isYourBrand", UNSET)

        is_ai_generated = d.pop("isAiGenerated", UNSET)

        auto_add_music = d.pop("autoAddMusic", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        tik_tok_options = cls(
            privacy_level=privacy_level,
            disabled_comments=disabled_comments,
            disabled_duet=disabled_duet,
            disabled_stitch=disabled_stitch,
            is_branded_content=is_branded_content,
            is_your_brand=is_your_brand,
            is_ai_generated=is_ai_generated,
            auto_add_music=auto_add_music,
            title=title,
            description=description,
        )

        tik_tok_options.additional_properties = d
        return tik_tok_options

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
