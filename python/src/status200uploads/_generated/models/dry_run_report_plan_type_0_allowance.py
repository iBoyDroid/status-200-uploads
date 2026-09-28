from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DryRunReportPlanType0Allowance")


@_attrs_define
class DryRunReportPlanType0Allowance:
    """
    Attributes:
        kind (str | Unset):
        used (int | None | Unset):
        limit (int | None | Unset):
        resets_at (None | str | Unset):
    """

    kind: str | Unset = UNSET
    used: int | None | Unset = UNSET
    limit: int | None | Unset = UNSET
    resets_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        used: int | None | Unset
        if isinstance(self.used, Unset):
            used = UNSET
        else:
            used = self.used

        limit: int | None | Unset
        if isinstance(self.limit, Unset):
            limit = UNSET
        else:
            limit = self.limit

        resets_at: None | str | Unset
        if isinstance(self.resets_at, Unset):
            resets_at = UNSET
        else:
            resets_at = self.resets_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if used is not UNSET:
            field_dict["used"] = used
        if limit is not UNSET:
            field_dict["limit"] = limit
        if resets_at is not UNSET:
            field_dict["resets_at"] = resets_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = d.pop("kind", UNSET)

        def _parse_used(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        used = _parse_used(d.pop("used", UNSET))

        def _parse_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        limit = _parse_limit(d.pop("limit", UNSET))

        def _parse_resets_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resets_at = _parse_resets_at(d.pop("resets_at", UNSET))

        dry_run_report_plan_type_0_allowance = cls(
            kind=kind,
            used=used,
            limit=limit,
            resets_at=resets_at,
        )

        dry_run_report_plan_type_0_allowance.additional_properties = d
        return dry_run_report_plan_type_0_allowance

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
