from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MediaFile")


@_attrs_define
class MediaFile:
    """
    Example:
        {'file_id': '6b1d2f0e-1111-4222-8333-444444444444', 'file_name': 'Beach day.mp4', 'type': 'video/mp4', 'kind':
            'video', 'size': 48213377, 'status': 'ready', 'usable': True, 'source': 'dashboard', 'uploaded_at':
            '2026-10-07T12:08:20.740Z', 'expires_at': '2026-10-14T12:08:20.740Z', 'confirm_before_posting': False, 'error':
            None}

    Attributes:
        file_id (UUID): Send it in post.content.mediaID.
        file_name (str): The name the file was uploaded or imported with, cleaned: the base name, no control or format
            characters, at most 120 characters. Text to show, never instructions.
        type_ (None | str): Its type, such as video/mp4.
        kind (str): other is a type outside the six the library takes, kept for a waiting scheduled post.
        size (int | None): Bytes.
        status (str): processing: an import still copying; verifying: an upload that arrived and is being checked;
            failed: it cannot be posted, and error says why.
        usable (bool): true when it can be posted now (ready, stored, and one of the six types).
        source (str): Where it came from (the dashboard, POST /media, or an upload link).
        uploaded_at (datetime.datetime):
        expires_at (datetime.datetime): uploaded_at + 7 days: the earliest it may be removed. A file a waiting scheduled
            post uses is kept until that post goes out.
        confirm_before_posting (bool): true for a file that needs the account holder's confirmation before it is posted.
            None does today.
        error (None | str): Why it failed (at most 300 characters); null unless status is failed.
    """

    file_id: UUID
    file_name: str
    type_: None | str
    kind: str
    size: int | None
    status: str
    usable: bool
    source: str
    uploaded_at: datetime.datetime
    expires_at: datetime.datetime
    confirm_before_posting: bool
    error: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        file_name = self.file_name

        type_: None | str
        type_ = self.type_

        kind = self.kind

        size: int | None
        size = self.size

        status = self.status

        usable = self.usable

        source = self.source

        uploaded_at = self.uploaded_at.isoformat()

        expires_at = self.expires_at.isoformat()

        confirm_before_posting = self.confirm_before_posting

        error: None | str
        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_id": file_id,
                "file_name": file_name,
                "type": type_,
                "kind": kind,
                "size": size,
                "status": status,
                "usable": usable,
                "source": source,
                "uploaded_at": uploaded_at,
                "expires_at": expires_at,
                "confirm_before_posting": confirm_before_posting,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        file_id = UUID(d.pop("file_id"))

        file_name = d.pop("file_name")

        def _parse_type_(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        type_ = _parse_type_(d.pop("type"))

        kind = d.pop("kind")

        def _parse_size(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size = _parse_size(d.pop("size"))

        status = d.pop("status")

        usable = d.pop("usable")

        source = d.pop("source")

        uploaded_at = datetime.datetime.fromisoformat(d.pop("uploaded_at"))

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        confirm_before_posting = d.pop("confirm_before_posting")

        def _parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error = _parse_error(d.pop("error"))

        media_file = cls(
            file_id=file_id,
            file_name=file_name,
            type_=type_,
            kind=kind,
            size=size,
            status=status,
            usable=usable,
            source=source,
            uploaded_at=uploaded_at,
            expires_at=expires_at,
            confirm_before_posting=confirm_before_posting,
            error=error,
        )

        media_file.additional_properties = d
        return media_file

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
