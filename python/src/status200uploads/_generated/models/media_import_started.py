from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MediaImportStarted")


@_attrs_define
class MediaImportStarted:
    """
    Attributes:
        success (bool):
        file_id (UUID):
        status (str):
        message (str):
        size (int | None):
        type_ (str):
    """

    success: bool
    file_id: UUID
    status: str
    message: str
    size: int | None
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        file_id = str(self.file_id)

        status = self.status

        message = self.message

        size: int | None
        size = self.size

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "file_id": file_id,
                "status": status,
                "message": message,
                "size": size,
                "type": type_,
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

        def _parse_size(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size = _parse_size(d.pop("size"))

        type_ = d.pop("type")

        media_import_started = cls(
            success=success,
            file_id=file_id,
            status=status,
            message=message,
            size=size,
            type_=type_,
        )

        media_import_started.additional_properties = d
        return media_import_started

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
