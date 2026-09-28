from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaStatus")


@_attrs_define
class MediaStatus:
    """
    Attributes:
        success (bool): true only when status is ready.
        file_id (UUID):
        status (str):
        size (int | None):
        type_ (None | str):
        public_url (None | str):
        error (None | str): The import's failure reason when status is failed. Not an error of this request.
        bytes_uploaded (int | Unset): Present when the size of a URL import is known.
        progress (int | Unset):
    """

    success: bool
    file_id: UUID
    status: str
    size: int | None
    type_: None | str
    public_url: None | str
    error: None | str
    bytes_uploaded: int | Unset = UNSET
    progress: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        file_id = str(self.file_id)

        status = self.status

        size: int | None
        size = self.size

        type_: None | str
        type_ = self.type_

        public_url: None | str
        public_url = self.public_url

        error: None | str
        error = self.error

        bytes_uploaded = self.bytes_uploaded

        progress = self.progress

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "file_id": file_id,
                "status": status,
                "size": size,
                "type": type_,
                "public_url": public_url,
                "error": error,
            }
        )
        if bytes_uploaded is not UNSET:
            field_dict["bytes_uploaded"] = bytes_uploaded
        if progress is not UNSET:
            field_dict["progress"] = progress

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        success = d.pop("success")

        file_id = UUID(d.pop("file_id"))

        status = d.pop("status")

        def _parse_size(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size = _parse_size(d.pop("size"))

        def _parse_type_(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        type_ = _parse_type_(d.pop("type"))

        def _parse_public_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        public_url = _parse_public_url(d.pop("public_url"))

        def _parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error = _parse_error(d.pop("error"))

        bytes_uploaded = d.pop("bytes_uploaded", UNSET)

        progress = d.pop("progress", UNSET)

        media_status = cls(
            success=success,
            file_id=file_id,
            status=status,
            size=size,
            type_=type_,
            public_url=public_url,
            error=error,
            bytes_uploaded=bytes_uploaded,
            progress=progress,
        )

        media_status.additional_properties = d
        return media_status

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
