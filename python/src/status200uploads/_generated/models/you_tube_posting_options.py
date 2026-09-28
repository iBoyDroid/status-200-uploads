from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.you_tube_posting_options_categories_item import (
        YouTubePostingOptionsCategoriesItem,
    )


T = TypeVar("T", bound="YouTubePostingOptions")


@_attrs_define
class YouTubePostingOptions:
    """
    Attributes:
        categories (list[YouTubePostingOptionsCategoriesItem] | Unset):
        privacy_status_options (list[str] | Unset):
        tags_max_characters (int | Unset):
    """

    categories: list[YouTubePostingOptionsCategoriesItem] | Unset = UNSET
    privacy_status_options: list[str] | Unset = UNSET
    tags_max_characters: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        categories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        privacy_status_options: list[str] | Unset = UNSET
        if not isinstance(self.privacy_status_options, Unset):
            privacy_status_options = self.privacy_status_options

        tags_max_characters = self.tags_max_characters

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if categories is not UNSET:
            field_dict["categories"] = categories
        if privacy_status_options is not UNSET:
            field_dict["privacy_status_options"] = privacy_status_options
        if tags_max_characters is not UNSET:
            field_dict["tags_max_characters"] = tags_max_characters

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.you_tube_posting_options_categories_item import (
            YouTubePostingOptionsCategoriesItem,
        )

        d = dict(src_dict)
        _categories = d.pop("categories", UNSET)
        categories: list[YouTubePostingOptionsCategoriesItem] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = YouTubePostingOptionsCategoriesItem.from_dict(
                    categories_item_data
                )

                categories.append(categories_item)

        privacy_status_options = cast(list[str], d.pop("privacy_status_options", UNSET))

        tags_max_characters = d.pop("tags_max_characters", UNSET)

        you_tube_posting_options = cls(
            categories=categories,
            privacy_status_options=privacy_status_options,
            tags_max_characters=tags_max_characters,
        )

        you_tube_posting_options.additional_properties = d
        return you_tube_posting_options

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
