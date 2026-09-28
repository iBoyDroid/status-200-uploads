from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DryRunReportWarningsItem")


@_attrs_define
class DryRunReportWarningsItem:
    """
    Attributes:
        code (str):
        message (str):
        also_blocking (bool | Unset): A second refusal after the one in reason.
    """

    code: str
    message: str
    also_blocking: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        also_blocking = self.also_blocking

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if also_blocking is not UNSET:
            field_dict["also_blocking"] = also_blocking

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        also_blocking = d.pop("also_blocking", UNSET)

        dry_run_report_warnings_item = cls(
            code=code,
            message=message,
            also_blocking=also_blocking,
        )

        dry_run_report_warnings_item.additional_properties = d
        return dry_run_report_warnings_item

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
