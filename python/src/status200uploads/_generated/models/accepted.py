from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.accepted_data import AcceptedData
    from ..models.status_200_ids import Status200Ids
    from ..models.warning import Warning_


T = TypeVar("T", bound="Accepted")


@_attrs_define
class Accepted:
    """
    Attributes:
        code (str | Unset):
        message (str | Unset):
        data (AcceptedData | Unset):
        scheduled (bool | Unset): true on a scheduled post (code scheduled).
        queued (bool | Unset): true only when the daily allowance moved the post to the next UTC day.
        scheduled_post_id (UUID | Unset): DELETE /posts/{scheduled_post_id} cancels it.
        scheduled_at (datetime.datetime | Unset):
        platform (str | Unset):
        profile_id (UUID | Unset):
        upgrade_url (str | Unset):
        limit (int | Unset):
        used (int | Unset):
        plan (str | Unset):
        success (bool | Unset): false on still_publishing and schedule_unconfirmed (the outcome is not known yet).
        status (str | Unset):
        retry (bool | Unset): Always false, on still_publishing and schedule_unconfirmed only: do not send this request
            again. A boolean, not a rule (REST refusals carry no retry field).
        post_id (UUID | Unset): still_publishing, when the post is already in History.
        warnings (list[Warning_] | Unset):
        status200 (Status200Ids | Unset): Our ids, on every answer (any status) that recorded a post in History or a
            scheduled post; never on a dry run or on a refusal that recorded nothing. Use it rather than data.post_id, which
            is the network's own id on Facebook, LinkedIn and Skool.
    """

    code: str | Unset = UNSET
    message: str | Unset = UNSET
    data: AcceptedData | Unset = UNSET
    scheduled: bool | Unset = UNSET
    queued: bool | Unset = UNSET
    scheduled_post_id: UUID | Unset = UNSET
    scheduled_at: datetime.datetime | Unset = UNSET
    platform: str | Unset = UNSET
    profile_id: UUID | Unset = UNSET
    upgrade_url: str | Unset = UNSET
    limit: int | Unset = UNSET
    used: int | Unset = UNSET
    plan: str | Unset = UNSET
    success: bool | Unset = UNSET
    status: str | Unset = UNSET
    retry: bool | Unset = UNSET
    post_id: UUID | Unset = UNSET
    warnings: list[Warning_] | Unset = UNSET
    status200: Status200Ids | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        scheduled = self.scheduled

        queued = self.queued

        scheduled_post_id: str | Unset = UNSET
        if not isinstance(self.scheduled_post_id, Unset):
            scheduled_post_id = str(self.scheduled_post_id)

        scheduled_at: str | Unset = UNSET
        if not isinstance(self.scheduled_at, Unset):
            scheduled_at = self.scheduled_at.isoformat()

        platform = self.platform

        profile_id: str | Unset = UNSET
        if not isinstance(self.profile_id, Unset):
            profile_id = str(self.profile_id)

        upgrade_url = self.upgrade_url

        limit = self.limit

        used = self.used

        plan = self.plan

        success = self.success

        status = self.status

        retry = self.retry

        post_id: str | Unset = UNSET
        if not isinstance(self.post_id, Unset):
            post_id = str(self.post_id)

        warnings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = []
            for warnings_item_data in self.warnings:
                warnings_item = warnings_item_data.to_dict()
                warnings.append(warnings_item)

        status200: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status200, Unset):
            status200 = self.status200.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if message is not UNSET:
            field_dict["message"] = message
        if data is not UNSET:
            field_dict["data"] = data
        if scheduled is not UNSET:
            field_dict["scheduled"] = scheduled
        if queued is not UNSET:
            field_dict["queued"] = queued
        if scheduled_post_id is not UNSET:
            field_dict["scheduled_post_id"] = scheduled_post_id
        if scheduled_at is not UNSET:
            field_dict["scheduled_at"] = scheduled_at
        if platform is not UNSET:
            field_dict["platform"] = platform
        if profile_id is not UNSET:
            field_dict["profile_id"] = profile_id
        if upgrade_url is not UNSET:
            field_dict["upgrade_url"] = upgrade_url
        if limit is not UNSET:
            field_dict["limit"] = limit
        if used is not UNSET:
            field_dict["used"] = used
        if plan is not UNSET:
            field_dict["plan"] = plan
        if success is not UNSET:
            field_dict["success"] = success
        if status is not UNSET:
            field_dict["status"] = status
        if retry is not UNSET:
            field_dict["retry"] = retry
        if post_id is not UNSET:
            field_dict["post_id"] = post_id
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if status200 is not UNSET:
            field_dict["status200"] = status200

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.accepted_data import AcceptedData
        from ..models.status_200_ids import Status200Ids
        from ..models.warning import Warning_

        d = dict(src_dict)
        code = d.pop("code", UNSET)

        message = d.pop("message", UNSET)

        _data = d.pop("data", UNSET)
        data: AcceptedData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = AcceptedData.from_dict(_data)

        scheduled = d.pop("scheduled", UNSET)

        queued = d.pop("queued", UNSET)

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

        platform = d.pop("platform", UNSET)

        _profile_id = d.pop("profile_id", UNSET)
        profile_id: UUID | Unset
        if isinstance(_profile_id, Unset):
            profile_id = UNSET
        else:
            profile_id = UUID(_profile_id)

        upgrade_url = d.pop("upgrade_url", UNSET)

        limit = d.pop("limit", UNSET)

        used = d.pop("used", UNSET)

        plan = d.pop("plan", UNSET)

        success = d.pop("success", UNSET)

        status = d.pop("status", UNSET)

        retry = d.pop("retry", UNSET)

        _post_id = d.pop("post_id", UNSET)
        post_id: UUID | Unset
        if isinstance(_post_id, Unset):
            post_id = UNSET
        else:
            post_id = UUID(_post_id)

        _warnings = d.pop("warnings", UNSET)
        warnings: list[Warning_] | Unset = UNSET
        if _warnings is not UNSET:
            warnings = []
            for warnings_item_data in _warnings:
                warnings_item = Warning_.from_dict(warnings_item_data)

                warnings.append(warnings_item)

        _status200 = d.pop("status200", UNSET)
        status200: Status200Ids | Unset
        if isinstance(_status200, Unset):
            status200 = UNSET
        else:
            status200 = Status200Ids.from_dict(_status200)

        accepted = cls(
            code=code,
            message=message,
            data=data,
            scheduled=scheduled,
            queued=queued,
            scheduled_post_id=scheduled_post_id,
            scheduled_at=scheduled_at,
            platform=platform,
            profile_id=profile_id,
            upgrade_url=upgrade_url,
            limit=limit,
            used=used,
            plan=plan,
            success=success,
            status=status,
            retry=retry,
            post_id=post_id,
            warnings=warnings,
            status200=status200,
        )

        accepted.additional_properties = d
        return accepted

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
