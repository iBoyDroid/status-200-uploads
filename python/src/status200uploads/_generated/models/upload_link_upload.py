from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadLinkUpload")


@_attrs_define
class UploadLinkUpload:
    """
    Attributes:
        protocol (str):
        url (str): The TUS upload address, on storage's own host (yglvofckrdutesfzxwyb.storage.supabase.co). It names a
            private staging place, never the file_id or the file's public address.
        token (str): The signed upload token: send it as the x-signature header of every request to upload.url, never in
            a URL. It works for this one file only, for about 2 hours. Keep it out of logs and chat messages.
        chunk_size (int): Every PATCH but the last carries exactly this many bytes (6,291,456).
        token_expires_at (datetime.datetime | None):
        upload_expires_at (datetime.datetime | None): When storage drops the unfinished upload (about 24 hours after the
            link was made).
        resume_before (datetime.datetime | None): Until when a stopped upload can be continued (with a fresh token once
            this one expired): 2 hours after the newest token expires, at most 24 hours after the link was made. After it,
            what was sent is deleted.
    """

    protocol: str
    url: str
    token: str
    chunk_size: int
    token_expires_at: datetime.datetime | None
    upload_expires_at: datetime.datetime | None
    resume_before: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        protocol = self.protocol

        url = self.url

        token = self.token

        chunk_size = self.chunk_size

        token_expires_at: None | str
        if isinstance(self.token_expires_at, datetime.datetime):
            token_expires_at = self.token_expires_at.isoformat()
        else:
            token_expires_at = self.token_expires_at

        upload_expires_at: None | str
        if isinstance(self.upload_expires_at, datetime.datetime):
            upload_expires_at = self.upload_expires_at.isoformat()
        else:
            upload_expires_at = self.upload_expires_at

        resume_before: None | str
        if isinstance(self.resume_before, datetime.datetime):
            resume_before = self.resume_before.isoformat()
        else:
            resume_before = self.resume_before

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "protocol": protocol,
                "url": url,
                "token": token,
                "chunk_size": chunk_size,
                "token_expires_at": token_expires_at,
                "upload_expires_at": upload_expires_at,
                "resume_before": resume_before,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        protocol = d.pop("protocol")

        url = d.pop("url")

        token = d.pop("token")

        chunk_size = d.pop("chunk_size")

        def _parse_token_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                token_expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return token_expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        token_expires_at = _parse_token_expires_at(d.pop("token_expires_at"))

        def _parse_upload_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                upload_expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return upload_expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        upload_expires_at = _parse_upload_expires_at(d.pop("upload_expires_at"))

        def _parse_resume_before(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resume_before_type_0 = datetime.datetime.fromisoformat(data)

                return resume_before_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        resume_before = _parse_resume_before(d.pop("resume_before"))

        upload_link_upload = cls(
            protocol=protocol,
            url=url,
            token=token,
            chunk_size=chunk_size,
            token_expires_at=token_expires_at,
            upload_expires_at=upload_expires_at,
            resume_before=resume_before,
        )

        upload_link_upload.additional_properties = d
        return upload_link_upload

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
