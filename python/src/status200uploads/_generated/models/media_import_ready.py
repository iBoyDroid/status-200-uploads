from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MediaImportReady")


@_attrs_define
class MediaImportReady:
    """
    Example:
        {'success': True, 'file_id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'size': 2048576, 'type': 'image/jpeg',
            'status': 'ready'}

    Attributes:
        success (bool):
        file_id (UUID): Send it in post.content.mediaID.
        size (int | None):
        type_ (str):
        status (str):
    """

    success: bool
    file_id: UUID
    size: int | None
    type_: str
    status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        file_id = str(self.file_id)

        size: int | None
        size = self.size

        type_ = self.type_

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "file_id": file_id,
                "size": size,
                "type": type_,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        success = d.pop("success")

        file_id = UUID(d.pop("file_id"))

        def _parse_size(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size = _parse_size(d.pop("size"))

        type_ = d.pop("type")

        status = d.pop("status")

        media_import_ready = cls(
            success=success,
            file_id=file_id,
            size=size,
            type_=type_,
            status=status,
        )

        media_import_ready.additional_properties = d
        return media_import_ready

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
