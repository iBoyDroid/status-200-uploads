from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.skool_posting_options_groups_item import SkoolPostingOptionsGroupsItem
    from ..models.skool_posting_options_labels_type_0_item import SkoolPostingOptionsLabelsType0Item


T = TypeVar("T", bound="SkoolPostingOptions")


@_attrs_define
class SkoolPostingOptions:
    """
    Attributes:
        groups (list[SkoolPostingOptionsGroupsItem] | Unset):
        labels (list[SkoolPostingOptionsLabelsType0Item] | None | Unset):
        labels_for_group (None | str | Unset):
    """

    groups: list[SkoolPostingOptionsGroupsItem] | Unset = UNSET
    labels: list[SkoolPostingOptionsLabelsType0Item] | None | Unset = UNSET
    labels_for_group: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        groups: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()
                groups.append(groups_item)

        labels: list[dict[str, Any]] | None | Unset
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, list):
            labels = []
            for labels_type_0_item_data in self.labels:
                labels_type_0_item = labels_type_0_item_data.to_dict()
                labels.append(labels_type_0_item)

        else:
            labels = self.labels

        labels_for_group: None | str | Unset
        if isinstance(self.labels_for_group, Unset):
            labels_for_group = UNSET
        else:
            labels_for_group = self.labels_for_group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if groups is not UNSET:
            field_dict["groups"] = groups
        if labels is not UNSET:
            field_dict["labels"] = labels
        if labels_for_group is not UNSET:
            field_dict["labels_for_group"] = labels_for_group

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.skool_posting_options_groups_item import (
            SkoolPostingOptionsGroupsItem,
        )
        from ..models.skool_posting_options_labels_type_0_item import (
            SkoolPostingOptionsLabelsType0Item,
        )

        d = dict(src_dict)
        _groups = d.pop("groups", UNSET)
        groups: list[SkoolPostingOptionsGroupsItem] | Unset = UNSET
        if _groups is not UNSET:
            groups = []
            for groups_item_data in _groups:
                groups_item = SkoolPostingOptionsGroupsItem.from_dict(groups_item_data)

                groups.append(groups_item)

        def _parse_labels(data: object) -> list[SkoolPostingOptionsLabelsType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                labels_type_0 = []
                _labels_type_0 = data
                for labels_type_0_item_data in _labels_type_0:
                    labels_type_0_item = SkoolPostingOptionsLabelsType0Item.from_dict(
                        labels_type_0_item_data
                    )

                    labels_type_0.append(labels_type_0_item)

                return labels_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SkoolPostingOptionsLabelsType0Item] | None | Unset, data)

        labels = _parse_labels(d.pop("labels", UNSET))

        def _parse_labels_for_group(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        labels_for_group = _parse_labels_for_group(d.pop("labels_for_group", UNSET))

        skool_posting_options = cls(
            groups=groups,
            labels=labels,
            labels_for_group=labels_for_group,
        )

        skool_posting_options.additional_properties = d
        return skool_posting_options

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
