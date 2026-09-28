from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DryRunReportTarget")


@_attrs_define
class DryRunReportTarget:
    """
    Attributes:
        account_id (None | str):
        profile_id (None | str):
        platform (None | str):
    """

    account_id: None | str
    profile_id: None | str
    platform: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id: None | str
        account_id = self.account_id

        profile_id: None | str
        profile_id = self.profile_id

        platform: None | str
        platform = self.platform

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "profile_id": profile_id,
                "platform": platform,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_account_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        account_id = _parse_account_id(d.pop("account_id"))

        def _parse_profile_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profile_id = _parse_profile_id(d.pop("profile_id"))

        def _parse_platform(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        platform = _parse_platform(d.pop("platform"))

        dry_run_report_target = cls(
            account_id=account_id,
            profile_id=profile_id,
            platform=platform,
        )

        dry_run_report_target.additional_properties = d
        return dry_run_report_target

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
