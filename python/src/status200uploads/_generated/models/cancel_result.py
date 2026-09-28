from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cancel_result_data import CancelResultData


T = TypeVar("T", bound="CancelResult")


@_attrs_define
class CancelResult:
    """
    Example:
        {'data': {'scheduled_post_id': 'c3d4e5f6-a7b8-9012-cdef-123456789012', 'status': 'cancelled', 'platforms':
            ['tiktok'], 'was_due_at': '2026-10-01T09:00:00+00:00', 'message': 'Cancelled. It will not be published.'}}

    Attributes:
        data (CancelResultData):
    """

    data: CancelResultData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.cancel_result_data import CancelResultData

        d = dict(src_dict)
        data = CancelResultData.from_dict(d.pop("data"))

        cancel_result = cls(
            data=data,
        )

        cancel_result.additional_properties = d
        return cancel_result

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
