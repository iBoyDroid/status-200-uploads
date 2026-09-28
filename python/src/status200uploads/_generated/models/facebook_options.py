from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.facebook_options_post_type import (
    FacebookOptionsPostType,
    check_facebook_options_post_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FacebookOptions")


@_attrs_define
class FacebookOptions:
    """
    Attributes:
        post_type (FacebookOptionsPostType | Unset): Omitted, text when the post has no media field at all, video for
            one video file, otherwise photo (several images make one multi-photo post). Without a postType, a media field
            sent empty ([] or null) is 400.
        video_title (str | Unset): The title of a video post (defaults to the caption).
        url (str | Unset): A link for a text post (Facebook makes a link preview).
    """

    post_type: FacebookOptionsPostType | Unset = UNSET
    video_title: str | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post_type: str | Unset = UNSET
        if not isinstance(self.post_type, Unset):
            post_type = self.post_type

        video_title = self.video_title

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if post_type is not UNSET:
            field_dict["postType"] = post_type
        if video_title is not UNSET:
            field_dict["videoTitle"] = video_title
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _post_type = d.pop("postType", UNSET)
        post_type: FacebookOptionsPostType | Unset
        if isinstance(_post_type, Unset):
            post_type = UNSET
        else:
            post_type = check_facebook_options_post_type(_post_type)

        video_title = d.pop("videoTitle", UNSET)

        url = d.pop("url", UNSET)

        facebook_options = cls(
            post_type=post_type,
            video_title=video_title,
            url=url,
        )

        facebook_options.additional_properties = d
        return facebook_options

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
