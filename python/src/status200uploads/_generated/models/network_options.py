from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.network_options_options_type_0 import NetworkOptionsOptionsType0


T = TypeVar("T", bound="NetworkOptions")


@_attrs_define
class NetworkOptions:
    """
    Attributes:
        platform (str):
        status (str): Only ok carries options; every other status has a note saying why not.
        options (NetworkOptionsOptionsType0 | None): Shaped per network (x-status200-options-by-platform names each
            schema).
        note (None | str):
        checked_at (datetime.datetime | None):
        cached (bool):
        error_code (None | str):
    """

    platform: str
    status: str
    options: NetworkOptionsOptionsType0 | None
    note: None | str
    checked_at: datetime.datetime | None
    cached: bool
    error_code: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.network_options_options_type_0 import (
            NetworkOptionsOptionsType0,
        )

        platform = self.platform

        status = self.status

        options: dict[str, Any] | None
        if isinstance(self.options, NetworkOptionsOptionsType0):
            options = self.options.to_dict()
        else:
            options = self.options

        note: None | str
        note = self.note

        checked_at: None | str
        if isinstance(self.checked_at, datetime.datetime):
            checked_at = self.checked_at.isoformat()
        else:
            checked_at = self.checked_at

        cached = self.cached

        error_code: None | str
        error_code = self.error_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "platform": platform,
                "status": status,
                "options": options,
                "note": note,
                "checked_at": checked_at,
                "cached": cached,
                "error_code": error_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.network_options_options_type_0 import (
            NetworkOptionsOptionsType0,
        )

        d = dict(src_dict)
        platform = d.pop("platform")

        status = d.pop("status")

        def _parse_options(data: object) -> NetworkOptionsOptionsType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_0 = NetworkOptionsOptionsType0.from_dict(data)

                return options_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(NetworkOptionsOptionsType0 | None, data)

        options = _parse_options(d.pop("options"))

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        def _parse_checked_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                checked_at_type_0 = datetime.datetime.fromisoformat(data)

                return checked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        checked_at = _parse_checked_at(d.pop("checked_at"))

        cached = d.pop("cached")

        def _parse_error_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_code = _parse_error_code(d.pop("error_code"))

        network_options = cls(
            platform=platform,
            status=status,
            options=options,
            note=note,
            checked_at=checked_at,
            cached=cached,
            error_code=error_code,
        )

        network_options.additional_properties = d
        return network_options

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
