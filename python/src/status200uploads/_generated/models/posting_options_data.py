from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.network_options import NetworkOptions


T = TypeVar("T", bound="PostingOptionsData")


@_attrs_define
class PostingOptionsData:
    """
    Attributes:
        profile_id (UUID):
        profile_name (str):
        networks (list[NetworkOptions]):
        note (None | str):
        asked_at (datetime.datetime):
    """

    profile_id: UUID
    profile_name: str
    networks: list[NetworkOptions]
    note: None | str
    asked_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile_id = str(self.profile_id)

        profile_name = self.profile_name

        networks = []
        for networks_item_data in self.networks:
            networks_item = networks_item_data.to_dict()
            networks.append(networks_item)

        note: None | str
        note = self.note

        asked_at = self.asked_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile_id": profile_id,
                "profile_name": profile_name,
                "networks": networks,
                "note": note,
                "asked_at": asked_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.network_options import NetworkOptions

        d = dict(src_dict)
        profile_id = UUID(d.pop("profile_id"))

        profile_name = d.pop("profile_name")

        networks = []
        _networks = d.pop("networks")
        for networks_item_data in _networks:
            networks_item = NetworkOptions.from_dict(networks_item_data)

            networks.append(networks_item)

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        asked_at = datetime.datetime.fromisoformat(d.pop("asked_at"))

        posting_options_data = cls(
            profile_id=profile_id,
            profile_name=profile_name,
            networks=networks,
            note=note,
            asked_at=asked_at,
        )

        posting_options_data.additional_properties = d
        return posting_options_data

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
