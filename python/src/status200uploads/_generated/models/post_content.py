from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostContent")


@_attrs_define
class PostContent:
    """
    Attributes:
        text (str | Unset): The caption, post text or title. Required when the post has no media. On YouTube and TikTok
            photo posts it fills the title or the description you do not send.
        media_urls (list[str] | Unset): Public URLs of the files. Whether a file is an image or a video is read from the
            end of its URL (.jpg, .png, .mp4 ...). A scheduled post fetches them when it goes out, not now (warning
            media_url_not_kept). Not used when file ids are sent too.
        media_id (list[str] | Unset): File ids from POST /media (UUIDs; also read as mediaIds). Used first, before
            mediaUrls. An id that does not exist on your account is 404 media_not_found; one still importing is waited for,
            then 409 media_processing. A value sent as text instead of a list is 400.
    """

    text: str | Unset = UNSET
    media_urls: list[str] | Unset = UNSET
    media_id: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        media_urls: list[str] | Unset = UNSET
        if not isinstance(self.media_urls, Unset):
            media_urls = self.media_urls

        media_id: list[str] | Unset = UNSET
        if not isinstance(self.media_id, Unset):
            media_id = self.media_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text is not UNSET:
            field_dict["text"] = text
        if media_urls is not UNSET:
            field_dict["mediaUrls"] = media_urls
        if media_id is not UNSET:
            field_dict["mediaID"] = media_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        text = d.pop("text", UNSET)

        media_urls = cast(list[str], d.pop("mediaUrls", UNSET))

        media_id = cast(list[str], d.pop("mediaID", UNSET))

        post_content = cls(
            text=text,
            media_urls=media_urls,
            media_id=media_id,
        )

        post_content.additional_properties = d
        return post_content

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
