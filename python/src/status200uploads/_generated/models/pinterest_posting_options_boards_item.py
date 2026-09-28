from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PinterestPostingOptionsBoardsItem")


@_attrs_define
class PinterestPostingOptionsBoardsItem:
    """
    Attributes:
        id (None | str | Unset): Send it as post.pinterest.boardId.
        name (None | str | Unset):
        privacy (None | str | Unset):
        pin_count (float | None | Unset):
    """

    id: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    privacy: None | str | Unset = UNSET
    pin_count: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        privacy: None | str | Unset
        if isinstance(self.privacy, Unset):
            privacy = UNSET
        else:
            privacy = self.privacy

        pin_count: float | None | Unset
        if isinstance(self.pin_count, Unset):
            pin_count = UNSET
        else:
            pin_count = self.pin_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if privacy is not UNSET:
            field_dict["privacy"] = privacy
        if pin_count is not UNSET:
            field_dict["pin_count"] = pin_count

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_privacy(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        privacy = _parse_privacy(d.pop("privacy", UNSET))

        def _parse_pin_count(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        pin_count = _parse_pin_count(d.pop("pin_count", UNSET))

        pinterest_posting_options_boards_item = cls(
            id=id,
            name=name,
            privacy=privacy,
            pin_count=pin_count,
        )

        pinterest_posting_options_boards_item.additional_properties = d
        return pinterest_posting_options_boards_item

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
