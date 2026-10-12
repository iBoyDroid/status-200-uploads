from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadLinkError")


@_attrs_define
class UploadLinkError:
    """The refusals of the upload-link endpoints. Besides the fields here they carry next_step (what to do next, in a
    sentence) and, for most codes, retry: "never" (the same request cannot succeed now) or "after_reset" (a budget that
    frees at 00:00 UTC). The AI connector reads the same answers; what a client may send again is
    components.x-status200-retry.

        Attributes:
            code (str): Branch on this. Each response lists its codes in x-error-codes; new codes are added without notice.
            message (str): A sentence for a person, saying what happened.
            file_id (UUID | Unset):
            reason (None | str | Unset): upload_rejected and upload_failed - why. sha256 or size: the file that arrived is
                not the one measured (measure it again, and do not upload it again when the values are the same). type or
                content: it is not really a file of its type (renaming does not change that). replaced, conflict or gone: make a
                new link. unverifiable (upload_failed): it could not be checked within 24 hours because of a problem on our
                side.
            retry_after_seconds (int | Unset): Seconds to wait before the same request can succeed; the Retry-After header
                says the same when it is an hour or less.
            plan (str | Unset):
            upgrade_url (str | Unset):
            open_ (int | Unset):
            limit (int | Unset):
            window (str | Unset):
            resets_at (datetime.datetime | None | Unset):
            used_bytes (int | Unset):
            limit_bytes (int | Unset):
            remaining_bytes (int | Unset):
            requested_bytes (int | Unset):
            held_bytes (int | Unset): import_budget_exhausted - the bytes of today's budget held by unfinished upload links
                of this account whose file has not fully arrived (only when there are any).
            held_until (datetime.datetime | Unset): import_budget_exhausted - when those links free their bytes if nobody
                continues them (only when that is before resets_at).
            size_bytes (int | Unset):
            max_bytes (int | Unset):
    """

    code: str
    message: str
    file_id: UUID | Unset = UNSET
    reason: None | str | Unset = UNSET
    retry_after_seconds: int | Unset = UNSET
    plan: str | Unset = UNSET
    upgrade_url: str | Unset = UNSET
    open_: int | Unset = UNSET
    limit: int | Unset = UNSET
    window: str | Unset = UNSET
    resets_at: datetime.datetime | None | Unset = UNSET
    used_bytes: int | Unset = UNSET
    limit_bytes: int | Unset = UNSET
    remaining_bytes: int | Unset = UNSET
    requested_bytes: int | Unset = UNSET
    held_bytes: int | Unset = UNSET
    held_until: datetime.datetime | Unset = UNSET
    size_bytes: int | Unset = UNSET
    max_bytes: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        file_id: str | Unset = UNSET
        if not isinstance(self.file_id, Unset):
            file_id = str(self.file_id)

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        retry_after_seconds = self.retry_after_seconds

        plan = self.plan

        upgrade_url = self.upgrade_url

        open_ = self.open_

        limit = self.limit

        window = self.window

        resets_at: None | str | Unset
        if isinstance(self.resets_at, Unset):
            resets_at = UNSET
        elif isinstance(self.resets_at, datetime.datetime):
            resets_at = self.resets_at.isoformat()
        else:
            resets_at = self.resets_at

        used_bytes = self.used_bytes

        limit_bytes = self.limit_bytes

        remaining_bytes = self.remaining_bytes

        requested_bytes = self.requested_bytes

        held_bytes = self.held_bytes

        held_until: str | Unset = UNSET
        if not isinstance(self.held_until, Unset):
            held_until = self.held_until.isoformat()

        size_bytes = self.size_bytes

        max_bytes = self.max_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if file_id is not UNSET:
            field_dict["file_id"] = file_id
        if reason is not UNSET:
            field_dict["reason"] = reason
        if retry_after_seconds is not UNSET:
            field_dict["retry_after_seconds"] = retry_after_seconds
        if plan is not UNSET:
            field_dict["plan"] = plan
        if upgrade_url is not UNSET:
            field_dict["upgrade_url"] = upgrade_url
        if open_ is not UNSET:
            field_dict["open"] = open_
        if limit is not UNSET:
            field_dict["limit"] = limit
        if window is not UNSET:
            field_dict["window"] = window
        if resets_at is not UNSET:
            field_dict["resets_at"] = resets_at
        if used_bytes is not UNSET:
            field_dict["used_bytes"] = used_bytes
        if limit_bytes is not UNSET:
            field_dict["limit_bytes"] = limit_bytes
        if remaining_bytes is not UNSET:
            field_dict["remaining_bytes"] = remaining_bytes
        if requested_bytes is not UNSET:
            field_dict["requested_bytes"] = requested_bytes
        if held_bytes is not UNSET:
            field_dict["held_bytes"] = held_bytes
        if held_until is not UNSET:
            field_dict["held_until"] = held_until
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if max_bytes is not UNSET:
            field_dict["max_bytes"] = max_bytes

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        _file_id = d.pop("file_id", UNSET)
        file_id: UUID | Unset
        if isinstance(_file_id, Unset):
            file_id = UNSET
        else:
            file_id = UUID(_file_id)

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        retry_after_seconds = d.pop("retry_after_seconds", UNSET)

        plan = d.pop("plan", UNSET)

        upgrade_url = d.pop("upgrade_url", UNSET)

        open_ = d.pop("open", UNSET)

        limit = d.pop("limit", UNSET)

        window = d.pop("window", UNSET)

        def _parse_resets_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resets_at_type_0 = datetime.datetime.fromisoformat(data)

                return resets_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        resets_at = _parse_resets_at(d.pop("resets_at", UNSET))

        used_bytes = d.pop("used_bytes", UNSET)

        limit_bytes = d.pop("limit_bytes", UNSET)

        remaining_bytes = d.pop("remaining_bytes", UNSET)

        requested_bytes = d.pop("requested_bytes", UNSET)

        held_bytes = d.pop("held_bytes", UNSET)

        _held_until = d.pop("held_until", UNSET)
        held_until: datetime.datetime | Unset
        if isinstance(_held_until, Unset):
            held_until = UNSET
        else:
            held_until = datetime.datetime.fromisoformat(_held_until)

        size_bytes = d.pop("size_bytes", UNSET)

        max_bytes = d.pop("max_bytes", UNSET)

        upload_link_error = cls(
            code=code,
            message=message,
            file_id=file_id,
            reason=reason,
            retry_after_seconds=retry_after_seconds,
            plan=plan,
            upgrade_url=upgrade_url,
            open_=open_,
            limit=limit,
            window=window,
            resets_at=resets_at,
            used_bytes=used_bytes,
            limit_bytes=limit_bytes,
            remaining_bytes=remaining_bytes,
            requested_bytes=requested_bytes,
            held_bytes=held_bytes,
            held_until=held_until,
            size_bytes=size_bytes,
            max_bytes=max_bytes,
        )

        upload_link_error.additional_properties = d
        return upload_link_error

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
