from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SkoolOptions")


@_attrs_define
class SkoolOptions:
    """
    Attributes:
        group (str | Unset): Required. The Skool group id (GET /accounts/{profile_id}/options lists the groups).
        group_slug (str | Unset):
        label (str | Unset): A category label id.
        title (str | Unset): Required. The post title.
    """

    group: str | Unset = UNSET
    group_slug: str | Unset = UNSET
    label: str | Unset = UNSET
    title: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group = self.group

        group_slug = self.group_slug

        label = self.label

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if group is not UNSET:
            field_dict["group"] = group
        if group_slug is not UNSET:
            field_dict["groupSlug"] = group_slug
        if label is not UNSET:
            field_dict["label"] = label
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        group = d.pop("group", UNSET)

        group_slug = d.pop("groupSlug", UNSET)

        label = d.pop("label", UNSET)

        title = d.pop("title", UNSET)

        skool_options = cls(
            group=group,
            group_slug=group_slug,
            label=label,
            title=title,
        )

        skool_options.additional_properties = d
        return skool_options

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
