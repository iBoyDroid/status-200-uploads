from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadVerifying")


@_attrs_define
class UploadVerifying:
    """
    Attributes:
        success (bool):
        file_id (UUID):
        status (str):
        file_name (str):
        size (int):
        type_ (str):
        sha256 (str):
        message (str):
        retry_after_seconds (int): The same seconds as Retry-After. 15, or longer when a temporary problem on our side
            delayed the check (it retries on its own).
    """

    success: bool
    file_id: UUID
    status: str
    file_name: str
    size: int
    type_: str
    sha256: str
    message: str
    retry_after_seconds: int
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

        retry_after_seconds = self.retry_after_seconds

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
                "retry_after_seconds": retry_after_seconds,
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

        retry_after_seconds = d.pop("retry_after_seconds")

        upload_verifying = cls(
            success=success,
            file_id=file_id,
            status=status,
            file_name=file_name,
            size=size,
            type_=type_,
            sha256=sha256,
            message=message,
            retry_after_seconds=retry_after_seconds,
        )

        upload_verifying.additional_properties = d
        return upload_verifying

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
