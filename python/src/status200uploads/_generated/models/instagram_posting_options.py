from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstagramPostingOptions")


@_attrs_define
class InstagramPostingOptions:
    """Instagram's rolling publishing limit. A null means Instagram did not report it, not a zero.

    Attributes:
        posts_used (float | None | Unset):
        posts_allowed (float | None | Unset):
        posts_left (float | None | Unset):
        window_hours (float | None | Unset):
    """

    posts_used: float | None | Unset = UNSET
    posts_allowed: float | None | Unset = UNSET
    posts_left: float | None | Unset = UNSET
    window_hours: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        posts_used: float | None | Unset
        if isinstance(self.posts_used, Unset):
            posts_used = UNSET
        else:
            posts_used = self.posts_used

        posts_allowed: float | None | Unset
        if isinstance(self.posts_allowed, Unset):
            posts_allowed = UNSET
        else:
            posts_allowed = self.posts_allowed

        posts_left: float | None | Unset
        if isinstance(self.posts_left, Unset):
            posts_left = UNSET
        else:
            posts_left = self.posts_left

        window_hours: float | None | Unset
        if isinstance(self.window_hours, Unset):
            window_hours = UNSET
        else:
            window_hours = self.window_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if posts_used is not UNSET:
            field_dict["posts_used"] = posts_used
        if posts_allowed is not UNSET:
            field_dict["posts_allowed"] = posts_allowed
        if posts_left is not UNSET:
            field_dict["posts_left"] = posts_left
        if window_hours is not UNSET:
            field_dict["window_hours"] = window_hours

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_posts_used(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        posts_used = _parse_posts_used(d.pop("posts_used", UNSET))

        def _parse_posts_allowed(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        posts_allowed = _parse_posts_allowed(d.pop("posts_allowed", UNSET))

        def _parse_posts_left(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        posts_left = _parse_posts_left(d.pop("posts_left", UNSET))

        def _parse_window_hours(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        window_hours = _parse_window_hours(d.pop("window_hours", UNSET))

        instagram_posting_options = cls(
            posts_used=posts_used,
            posts_allowed=posts_allowed,
            posts_left=posts_left,
            window_hours=window_hours,
        )

        instagram_posting_options.additional_properties = d
        return instagram_posting_options

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
