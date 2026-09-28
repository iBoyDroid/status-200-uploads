from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_network import AccountNetwork


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """
    Attributes:
        profile_id (UUID):
        profile_name (str):
        handle (str): "@" and the profile name: usable as post.accountId.
        created_at (datetime.datetime | None):
        networks (list[AccountNetwork]):
    """

    profile_id: UUID
    profile_name: str
    handle: str
    created_at: datetime.datetime | None
    networks: list[AccountNetwork]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile_id = str(self.profile_id)

        profile_name = self.profile_name

        handle = self.handle

        created_at: None | str
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        networks = []
        for networks_item_data in self.networks:
            networks_item = networks_item_data.to_dict()
            networks.append(networks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile_id": profile_id,
                "profile_name": profile_name,
                "handle": handle,
                "created_at": created_at,
                "networks": networks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.account_network import AccountNetwork

        d = dict(src_dict)
        profile_id = UUID(d.pop("profile_id"))

        profile_name = d.pop("profile_name")

        handle = d.pop("handle")

        def _parse_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        created_at = _parse_created_at(d.pop("created_at"))

        networks = []
        _networks = d.pop("networks")
        for networks_item_data in _networks:
            networks_item = AccountNetwork.from_dict(networks_item_data)

            networks.append(networks_item)

        account = cls(
            profile_id=profile_id,
            profile_name=profile_name,
            handle=handle,
            created_at=created_at,
            networks=networks,
        )

        account.additional_properties = d
        return account

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
