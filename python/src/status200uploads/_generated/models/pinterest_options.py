from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PinterestOptions")


@_attrs_define
class PinterestOptions:
    """
    Attributes:
        board_id (str | Unset): Required for a pin: Pinterest's id of the board (GET /accounts/{profile_id}/options
            lists the boards). Also read as board_id. Without it the post is 400 pinterest_board_required before Pinterest
            is called.
        title (str | Unset): Cut to 100 characters; content.text when omitted.
        description (str | Unset): Cut to 800 characters. Without it the pin has no description.
        link (str | Unset):
        alt_text (str | Unset):
        dominant_color (str | Unset): A hex colour such as '#FF5733'.
    """

    board_id: str | Unset = UNSET
    title: str | Unset = UNSET
    description: str | Unset = UNSET
    link: str | Unset = UNSET
    alt_text: str | Unset = UNSET
    dominant_color: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        board_id = self.board_id

        title = self.title

        description = self.description

        link = self.link

        alt_text = self.alt_text

        dominant_color = self.dominant_color

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if board_id is not UNSET:
            field_dict["boardId"] = board_id
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if link is not UNSET:
            field_dict["link"] = link
        if alt_text is not UNSET:
            field_dict["altText"] = alt_text
        if dominant_color is not UNSET:
            field_dict["dominantColor"] = dominant_color

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        board_id = d.pop("boardId", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        link = d.pop("link", UNSET)

        alt_text = d.pop("altText", UNSET)

        dominant_color = d.pop("dominantColor", UNSET)

        pinterest_options = cls(
            board_id=board_id,
            title=title,
            description=description,
            link=link,
            alt_text=alt_text,
            dominant_color=dominant_color,
        )

        pinterest_options.additional_properties = d
        return pinterest_options

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
