from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountNetwork")


@_attrs_define
class AccountNetwork:
    """
    Attributes:
        platform (str):
        username (None | str):
        status (str): The connection's own status.
        health (str): ready = it can post now (a sign-in the network renews by itself on the next post included);
            reconnect_required = reconnect it on the Connections page.
        access_expires_at (datetime.datetime | None):
        connected_at (datetime.datetime | None):
        updated_at (datetime.datetime | None):
    """

    platform: str
    username: None | str
    status: str
    health: str
    access_expires_at: datetime.datetime | None
    connected_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        platform = self.platform

        username: None | str
        username = self.username

        status = self.status

        health = self.health

        access_expires_at: None | str
        if isinstance(self.access_expires_at, datetime.datetime):
            access_expires_at = self.access_expires_at.isoformat()
        else:
            access_expires_at = self.access_expires_at

        connected_at: None | str
        if isinstance(self.connected_at, datetime.datetime):
            connected_at = self.connected_at.isoformat()
        else:
            connected_at = self.connected_at

        updated_at: None | str
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "platform": platform,
                "username": username,
                "status": status,
                "health": health,
                "access_expires_at": access_expires_at,
                "connected_at": connected_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        platform = d.pop("platform")

        def _parse_username(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        username = _parse_username(d.pop("username"))

        status = d.pop("status")

        health = d.pop("health")

        def _parse_access_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                access_expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return access_expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        access_expires_at = _parse_access_expires_at(d.pop("access_expires_at"))

        def _parse_connected_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                connected_at_type_0 = datetime.datetime.fromisoformat(data)

                return connected_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        connected_at = _parse_connected_at(d.pop("connected_at"))

        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updated_at"))

        account_network = cls(
            platform=platform,
            username=username,
            status=status,
            health=health,
            access_expires_at=access_expires_at,
            connected_at=connected_at,
            updated_at=updated_at,
        )

        account_network.additional_properties = d
        return account_network

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
