from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dry_run_report_plan_type_0_allowance import DryRunReportPlanType0Allowance


T = TypeVar("T", bound="DryRunReportPlanType0")


@_attrs_define
class DryRunReportPlanType0:
    """
    Attributes:
        tier (str | Unset):
        is_admin (bool | Unset):
        allowance (DryRunReportPlanType0Allowance | Unset):
    """

    tier: str | Unset = UNSET
    is_admin: bool | Unset = UNSET
    allowance: DryRunReportPlanType0Allowance | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tier = self.tier

        is_admin = self.is_admin

        allowance: dict[str, Any] | Unset = UNSET
        if not isinstance(self.allowance, Unset):
            allowance = self.allowance.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tier is not UNSET:
            field_dict["tier"] = tier
        if is_admin is not UNSET:
            field_dict["is_admin"] = is_admin
        if allowance is not UNSET:
            field_dict["allowance"] = allowance

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.dry_run_report_plan_type_0_allowance import (
            DryRunReportPlanType0Allowance,
        )

        d = dict(src_dict)
        tier = d.pop("tier", UNSET)

        is_admin = d.pop("is_admin", UNSET)

        _allowance = d.pop("allowance", UNSET)
        allowance: DryRunReportPlanType0Allowance | Unset
        if isinstance(_allowance, Unset):
            allowance = UNSET
        else:
            allowance = DryRunReportPlanType0Allowance.from_dict(_allowance)

        dry_run_report_plan_type_0 = cls(
            tier=tier,
            is_admin=is_admin,
            allowance=allowance,
        )

        dry_run_report_plan_type_0.additional_properties = d
        return dry_run_report_plan_type_0

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
