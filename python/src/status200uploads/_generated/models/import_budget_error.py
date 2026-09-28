from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportBudgetError")


@_attrs_define
class ImportBudgetError:
    """The daily import budget of a connected AI app's key (managed keys only; an ordinary API key never meets it).

    Attributes:
        code (str):
        message (str):
        used_bytes (int | Unset):
        limit_bytes (int | None | Unset):
        remaining_bytes (int | Unset):
        requested_bytes (int | None | Unset):
        window (str | Unset):
        resets_at (datetime.datetime | Unset):
        plan (str | Unset):
        upgrade_url (str | Unset):
        retry_after_seconds (int | Unset):
    """

    code: str
    message: str
    used_bytes: int | Unset = UNSET
    limit_bytes: int | None | Unset = UNSET
    remaining_bytes: int | Unset = UNSET
    requested_bytes: int | None | Unset = UNSET
    window: str | Unset = UNSET
    resets_at: datetime.datetime | Unset = UNSET
    plan: str | Unset = UNSET
    upgrade_url: str | Unset = UNSET
    retry_after_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        used_bytes = self.used_bytes

        limit_bytes: int | None | Unset
        if isinstance(self.limit_bytes, Unset):
            limit_bytes = UNSET
        else:
            limit_bytes = self.limit_bytes

        remaining_bytes = self.remaining_bytes

        requested_bytes: int | None | Unset
        if isinstance(self.requested_bytes, Unset):
            requested_bytes = UNSET
        else:
            requested_bytes = self.requested_bytes

        window = self.window

        resets_at: str | Unset = UNSET
        if not isinstance(self.resets_at, Unset):
            resets_at = self.resets_at.isoformat()

        plan = self.plan

        upgrade_url = self.upgrade_url

        retry_after_seconds = self.retry_after_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if used_bytes is not UNSET:
            field_dict["used_bytes"] = used_bytes
        if limit_bytes is not UNSET:
            field_dict["limit_bytes"] = limit_bytes
        if remaining_bytes is not UNSET:
            field_dict["remaining_bytes"] = remaining_bytes
        if requested_bytes is not UNSET:
            field_dict["requested_bytes"] = requested_bytes
        if window is not UNSET:
            field_dict["window"] = window
        if resets_at is not UNSET:
            field_dict["resets_at"] = resets_at
        if plan is not UNSET:
            field_dict["plan"] = plan
        if upgrade_url is not UNSET:
            field_dict["upgrade_url"] = upgrade_url
        if retry_after_seconds is not UNSET:
            field_dict["retry_after_seconds"] = retry_after_seconds

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        used_bytes = d.pop("used_bytes", UNSET)

        def _parse_limit_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        limit_bytes = _parse_limit_bytes(d.pop("limit_bytes", UNSET))

        remaining_bytes = d.pop("remaining_bytes", UNSET)

        def _parse_requested_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        requested_bytes = _parse_requested_bytes(d.pop("requested_bytes", UNSET))

        window = d.pop("window", UNSET)

        _resets_at = d.pop("resets_at", UNSET)
        resets_at: datetime.datetime | Unset
        if isinstance(_resets_at, Unset):
            resets_at = UNSET
        else:
            resets_at = datetime.datetime.fromisoformat(_resets_at)

        plan = d.pop("plan", UNSET)

        upgrade_url = d.pop("upgrade_url", UNSET)

        retry_after_seconds = d.pop("retry_after_seconds", UNSET)

        import_budget_error = cls(
            code=code,
            message=message,
            used_bytes=used_bytes,
            limit_bytes=limit_bytes,
            remaining_bytes=remaining_bytes,
            requested_bytes=requested_bytes,
            window=window,
            resets_at=resets_at,
            plan=plan,
            upgrade_url=upgrade_url,
            retry_after_seconds=retry_after_seconds,
        )

        import_budget_error.additional_properties = d
        return import_budget_error

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
