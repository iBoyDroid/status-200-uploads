from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FacebookPostingOptions")


@_attrs_define
class FacebookPostingOptions:
    """
    Attributes:
        page_id (None | str | Unset):
        page_name (None | str | Unset):
        category (None | str | Unset):
        followers (float | None | Unset):
    """

    page_id: None | str | Unset = UNSET
    page_name: None | str | Unset = UNSET
    category: None | str | Unset = UNSET
    followers: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page_id: None | str | Unset
        if isinstance(self.page_id, Unset):
            page_id = UNSET
        else:
            page_id = self.page_id

        page_name: None | str | Unset
        if isinstance(self.page_name, Unset):
            page_name = UNSET
        else:
            page_name = self.page_name

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        followers: float | None | Unset
        if isinstance(self.followers, Unset):
            followers = UNSET
        else:
            followers = self.followers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page_id is not UNSET:
            field_dict["page_id"] = page_id
        if page_name is not UNSET:
            field_dict["page_name"] = page_name
        if category is not UNSET:
            field_dict["category"] = category
        if followers is not UNSET:
            field_dict["followers"] = followers

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_page_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        page_id = _parse_page_id(d.pop("page_id", UNSET))

        def _parse_page_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        page_name = _parse_page_name(d.pop("page_name", UNSET))

        def _parse_category(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_followers(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        followers = _parse_followers(d.pop("followers", UNSET))

        facebook_posting_options = cls(
            page_id=page_id,
            page_name=page_name,
            category=category,
            followers=followers,
        )

        facebook_posting_options.additional_properties = d
        return facebook_posting_options

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
