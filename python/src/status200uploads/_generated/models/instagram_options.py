from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.instagram_options_post_type import (
    InstagramOptionsPostType,
    check_instagram_options_post_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="InstagramOptions")


@_attrs_define
class InstagramOptions:
    """
    Attributes:
        post_type (InstagramOptionsPostType | Unset): Omitted, carousel for two or more files, reel for a single video,
            otherwise feed_image.
        share_to_feed (bool | Unset): Reels only. Default: True.
        cover_url (str | Unset): A Reel's cover image URL (fetched by Instagram when the Reel goes out).
        thumb_offset (float | Unset): A Reel's thumbnail offset in milliseconds.
        collaborators (list[str] | Unset): Usernames to invite as collaborators.
        location_id (str | Unset): A Facebook location id (feed images).
    """

    post_type: InstagramOptionsPostType | Unset = UNSET
    share_to_feed: bool | Unset = True
    cover_url: str | Unset = UNSET
    thumb_offset: float | Unset = UNSET
    collaborators: list[str] | Unset = UNSET
    location_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post_type: str | Unset = UNSET
        if not isinstance(self.post_type, Unset):
            post_type = self.post_type

        share_to_feed = self.share_to_feed

        cover_url = self.cover_url

        thumb_offset = self.thumb_offset

        collaborators: list[str] | Unset = UNSET
        if not isinstance(self.collaborators, Unset):
            collaborators = self.collaborators

        location_id = self.location_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if post_type is not UNSET:
            field_dict["postType"] = post_type
        if share_to_feed is not UNSET:
            field_dict["shareToFeed"] = share_to_feed
        if cover_url is not UNSET:
            field_dict["coverUrl"] = cover_url
        if thumb_offset is not UNSET:
            field_dict["thumbOffset"] = thumb_offset
        if collaborators is not UNSET:
            field_dict["collaborators"] = collaborators
        if location_id is not UNSET:
            field_dict["locationId"] = location_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _post_type = d.pop("postType", UNSET)
        post_type: InstagramOptionsPostType | Unset
        if isinstance(_post_type, Unset):
            post_type = UNSET
        else:
            post_type = check_instagram_options_post_type(_post_type)

        share_to_feed = d.pop("shareToFeed", UNSET)

        cover_url = d.pop("coverUrl", UNSET)

        thumb_offset = d.pop("thumbOffset", UNSET)

        collaborators = cast(list[str], d.pop("collaborators", UNSET))

        location_id = d.pop("locationId", UNSET)

        instagram_options = cls(
            post_type=post_type,
            share_to_feed=share_to_feed,
            cover_url=cover_url,
            thumb_offset=thumb_offset,
            collaborators=collaborators,
            location_id=location_id,
        )

        instagram_options.additional_properties = d
        return instagram_options

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
