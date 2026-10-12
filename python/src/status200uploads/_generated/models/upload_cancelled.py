from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadCancelled")


@_attrs_define
class UploadCancelled:
    """
    Example:
        {'success': True, 'file_id': '6b1d2f0e-3c4a-4b5d-8e6f-7a8b9c0d1e2f', 'status': 'cancelled', 'message': 'The
            upload was cancelled. Anything that arrived is deleted within a few minutes.'}

    Attributes:
        success (bool):
        file_id (UUID):
        status (str):
        message (str):
    """

    success: bool
    file_id: UUID
    status: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        file_id = str(self.file_id)

        status = self.status

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "file_id": file_id,
                "status": status,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        success = d.pop("success")

        file_id = UUID(d.pop("file_id"))

        status = d.pop("status")

        message = d.pop("message")

        upload_cancelled = cls(
            success=success,
            file_id=file_id,
            status=status,
            message=message,
        )

        upload_cancelled.additional_properties = d
        return upload_cancelled

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
