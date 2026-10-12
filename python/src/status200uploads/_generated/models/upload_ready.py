from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadReady")


@_attrs_define
class UploadReady:
    """
    Example:
        {'success': True, 'file_id': '6b1d2f0e-3c4a-4b5d-8e6f-7a8b9c0d1e2f', 'status': 'ready', 'file_name': 'EP01.mp4',
            'size': 295698432, 'type': 'video/mp4', 'sha256':
            '9f2c4b6a8e0d1c3b5a7f9e1d3c5b7a9f0e2d4c6b8a0f1e3d5c7b9a1f3e5d7c9b', 'message': 'EP01.mp4 arrived complete
            (295,698,432 bytes, SHA-256 matches). Publish it with this file_id.'}

    Attributes:
        success (bool):
        file_id (UUID): Send it in post.content.mediaID.
        status (str):
        file_name (str):
        size (int):
        type_ (str):
        sha256 (str):
        message (str):
    """

    success: bool
    file_id: UUID
    status: str
    file_name: str
    size: int
    type_: str
    sha256: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        file_id = str(self.file_id)

        status = self.status

        file_name = self.file_name

        size = self.size

        type_ = self.type_

        sha256 = self.sha256

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "file_id": file_id,
                "status": status,
                "file_name": file_name,
                "size": size,
                "type": type_,
                "sha256": sha256,
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

        file_name = d.pop("file_name")

        size = d.pop("size")

        type_ = d.pop("type")

        sha256 = d.pop("sha256")

        message = d.pop("message")

        upload_ready = cls(
            success=success,
            file_id=file_id,
            status=status,
            file_name=file_name,
            size=size,
            type_=type_,
            sha256=sha256,
            message=message,
        )

        upload_ready.additional_properties = d
        return upload_ready

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
