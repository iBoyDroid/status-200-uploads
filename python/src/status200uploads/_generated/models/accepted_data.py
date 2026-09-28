from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AcceptedData")


@_attrs_define
class AcceptedData:
    """
    Attributes:
        status (str | Unset):
        post_id (None | str | Unset):
        job_id (None | str | Unset):
        message (str | Unset):
        scheduled_post_id (UUID | Unset):
        scheduled_at (datetime.datetime | Unset):
    """

    status: str | Unset = UNSET
    post_id: None | str | Unset = UNSET
    job_id: None | str | Unset = UNSET
    message: str | Unset = UNSET
    scheduled_post_id: UUID | Unset = UNSET
    scheduled_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        post_id: None | str | Unset
        if isinstance(self.post_id, Unset):
            post_id = UNSET
        else:
            post_id = self.post_id

        job_id: None | str | Unset
        if isinstance(self.job_id, Unset):
            job_id = UNSET
        else:
            job_id = self.job_id

        message = self.message

        scheduled_post_id: str | Unset = UNSET
        if not isinstance(self.scheduled_post_id, Unset):
            scheduled_post_id = str(self.scheduled_post_id)

        scheduled_at: str | Unset = UNSET
        if not isinstance(self.scheduled_at, Unset):
            scheduled_at = self.scheduled_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if post_id is not UNSET:
            field_dict["post_id"] = post_id
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if message is not UNSET:
            field_dict["message"] = message
        if scheduled_post_id is not UNSET:
            field_dict["scheduled_post_id"] = scheduled_post_id
        if scheduled_at is not UNSET:
            field_dict["scheduled_at"] = scheduled_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = d.pop("status", UNSET)

        def _parse_post_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        post_id = _parse_post_id(d.pop("post_id", UNSET))

        def _parse_job_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        job_id = _parse_job_id(d.pop("job_id", UNSET))

        message = d.pop("message", UNSET)

        _scheduled_post_id = d.pop("scheduled_post_id", UNSET)
        scheduled_post_id: UUID | Unset
        if isinstance(_scheduled_post_id, Unset):
            scheduled_post_id = UNSET
        else:
            scheduled_post_id = UUID(_scheduled_post_id)

        _scheduled_at = d.pop("scheduled_at", UNSET)
        scheduled_at: datetime.datetime | Unset
        if isinstance(_scheduled_at, Unset):
            scheduled_at = UNSET
        else:
            scheduled_at = datetime.datetime.fromisoformat(_scheduled_at)

        accepted_data = cls(
            status=status,
            post_id=post_id,
            job_id=job_id,
            message=message,
            scheduled_post_id=scheduled_post_id,
            scheduled_at=scheduled_at,
        )

        accepted_data.additional_properties = d
        return accepted_data

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
