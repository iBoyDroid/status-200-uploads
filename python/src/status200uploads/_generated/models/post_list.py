from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_item import PostItem
    from ..models.scheduled_post_item import ScheduledPostItem
    from ..models.warning import Warning_


T = TypeVar("T", bound="PostList")


@_attrs_define
class PostList:
    """
    Attributes:
        data (list[PostItem | ScheduledPostItem]):
        next_cursor (None | str):
        next_url (None | str): The next page with the same filters; null on the last page.
        warnings (list[Warning_] | Unset):
    """

    data: list[PostItem | ScheduledPostItem]
    next_cursor: None | str
    next_url: None | str
    warnings: list[Warning_] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.post_item import PostItem

        data = []
        for data_item_data in self.data:
            data_item: dict[str, Any]
            if isinstance(data_item_data, PostItem):
                data_item = data_item_data.to_dict()
            else:
                data_item = data_item_data.to_dict()

            data.append(data_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        next_url: None | str
        next_url = self.next_url

        warnings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = []
            for warnings_item_data in self.warnings:
                warnings_item = warnings_item_data.to_dict()
                warnings.append(warnings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "next_cursor": next_cursor,
                "next_url": next_url,
            }
        )
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.post_item import PostItem
        from ..models.scheduled_post_item import ScheduledPostItem
        from ..models.warning import Warning_

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:

            def _parse_data_item(data: object) -> PostItem | ScheduledPostItem:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_0 = PostItem.from_dict(data)

                    return data_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                data_item_type_1 = ScheduledPostItem.from_dict(data)

                return data_item_type_1

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        def _parse_next_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_url = _parse_next_url(d.pop("next_url"))

        _warnings = d.pop("warnings", UNSET)
        warnings: list[Warning_] | Unset = UNSET
        if _warnings is not UNSET:
            warnings = []
            for warnings_item_data in _warnings:
                warnings_item = Warning_.from_dict(warnings_item_data)

                warnings.append(warnings_item)

        post_list = cls(
            data=data,
            next_cursor=next_cursor,
            next_url=next_url,
            warnings=warnings,
        )

        post_list.additional_properties = d
        return post_list

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
