from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorObject")


@_attrs_define
class ErrorObject:
    """REST refusals carry code, message and, for a plan refusal, upgrade_url, plus the facts of the refusal below. They
    carry no next_step and no retry field (those are the AI connector's); what a client may send again is
    components.x-status200-retry.

        Attributes:
            code (str): Branch on this, not on the status alone. Each response lists its codes in x-error-codes; new codes
                are added without notice.
            message (str): A sentence for a person, saying what to do.
            profiles (list[str] | Unset): account_not_found and profile_name_ambiguous (the older address's 404 api_error
                too) - your profiles as "@name", at most 25.
            file_id (str | Unset):
            progress (int | None | Unset):
            retry_after_seconds (int | Unset): On every 429, and on the refusals that ask for a short wait.
            upgrade_url (str | Unset):
            required (str | Unset):
            platform (str | Unset):
            plan (str | Unset):
            used (int | Unset):
            limit (int | Unset):
            window (str | Unset):
            resets_at (datetime.datetime | Unset):
            trial_available (bool | Unset):
            reason (str | Unset):
            scheduled_for (Any | Unset): The post.scheduledFor value as it was sent.
            status (str | Unset): not_cancellable - the scheduled post's status.
            tags_length (int | Unset):
            max_tags_length (int | Unset):
            remove_tags (int | Unset):
            size_bytes (int | Unset):
            limits_url (str | Unset):
            max_video_bytes (int | None | Unset): MEDIA_TOO_LARGE - the network's video limit here; null when the network
                takes no video here (Pinterest).
            max_image_bytes (int | None | Unset): MEDIA_TOO_LARGE - the network's image limit; null when the network takes
                no image (YouTube).
            parameter (str | Unset): The reads' 400 - which parameter.
            started_at (str | Unset):
            first_used_at (str | Unset):
            url (str | Unset):
            field (str | Unset):
            upstream_status (int | Unset):
            attempts (int | Unset):
            ceiling (int | Unset):
            detected_links (list[str] | Unset):
            link_used (int | Unset):
            link_limit (int | Unset):
    """

    code: str
    message: str
    profiles: list[str] | Unset = UNSET
    file_id: str | Unset = UNSET
    progress: int | None | Unset = UNSET
    retry_after_seconds: int | Unset = UNSET
    upgrade_url: str | Unset = UNSET
    required: str | Unset = UNSET
    platform: str | Unset = UNSET
    plan: str | Unset = UNSET
    used: int | Unset = UNSET
    limit: int | Unset = UNSET
    window: str | Unset = UNSET
    resets_at: datetime.datetime | Unset = UNSET
    trial_available: bool | Unset = UNSET
    reason: str | Unset = UNSET
    scheduled_for: Any | Unset = UNSET
    status: str | Unset = UNSET
    tags_length: int | Unset = UNSET
    max_tags_length: int | Unset = UNSET
    remove_tags: int | Unset = UNSET
    size_bytes: int | Unset = UNSET
    limits_url: str | Unset = UNSET
    max_video_bytes: int | None | Unset = UNSET
    max_image_bytes: int | None | Unset = UNSET
    parameter: str | Unset = UNSET
    started_at: str | Unset = UNSET
    first_used_at: str | Unset = UNSET
    url: str | Unset = UNSET
    field: str | Unset = UNSET
    upstream_status: int | Unset = UNSET
    attempts: int | Unset = UNSET
    ceiling: int | Unset = UNSET
    detected_links: list[str] | Unset = UNSET
    link_used: int | Unset = UNSET
    link_limit: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        profiles: list[str] | Unset = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = self.profiles

        file_id = self.file_id

        progress: int | None | Unset
        if isinstance(self.progress, Unset):
            progress = UNSET
        else:
            progress = self.progress

        retry_after_seconds = self.retry_after_seconds

        upgrade_url = self.upgrade_url

        required = self.required

        platform = self.platform

        plan = self.plan

        used = self.used

        limit = self.limit

        window = self.window

        resets_at: str | Unset = UNSET
        if not isinstance(self.resets_at, Unset):
            resets_at = self.resets_at.isoformat()

        trial_available = self.trial_available

        reason = self.reason

        scheduled_for = self.scheduled_for

        status = self.status

        tags_length = self.tags_length

        max_tags_length = self.max_tags_length

        remove_tags = self.remove_tags

        size_bytes = self.size_bytes

        limits_url = self.limits_url

        max_video_bytes: int | None | Unset
        if isinstance(self.max_video_bytes, Unset):
            max_video_bytes = UNSET
        else:
            max_video_bytes = self.max_video_bytes

        max_image_bytes: int | None | Unset
        if isinstance(self.max_image_bytes, Unset):
            max_image_bytes = UNSET
        else:
            max_image_bytes = self.max_image_bytes

        parameter = self.parameter

        started_at = self.started_at

        first_used_at = self.first_used_at

        url = self.url

        field = self.field

        upstream_status = self.upstream_status

        attempts = self.attempts

        ceiling = self.ceiling

        detected_links: list[str] | Unset = UNSET
        if not isinstance(self.detected_links, Unset):
            detected_links = self.detected_links

        link_used = self.link_used

        link_limit = self.link_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if profiles is not UNSET:
            field_dict["profiles"] = profiles
        if file_id is not UNSET:
            field_dict["file_id"] = file_id
        if progress is not UNSET:
            field_dict["progress"] = progress
        if retry_after_seconds is not UNSET:
            field_dict["retry_after_seconds"] = retry_after_seconds
        if upgrade_url is not UNSET:
            field_dict["upgrade_url"] = upgrade_url
        if required is not UNSET:
            field_dict["required"] = required
        if platform is not UNSET:
            field_dict["platform"] = platform
        if plan is not UNSET:
            field_dict["plan"] = plan
        if used is not UNSET:
            field_dict["used"] = used
        if limit is not UNSET:
            field_dict["limit"] = limit
        if window is not UNSET:
            field_dict["window"] = window
        if resets_at is not UNSET:
            field_dict["resets_at"] = resets_at
        if trial_available is not UNSET:
            field_dict["trial_available"] = trial_available
        if reason is not UNSET:
            field_dict["reason"] = reason
        if scheduled_for is not UNSET:
            field_dict["scheduled_for"] = scheduled_for
        if status is not UNSET:
            field_dict["status"] = status
        if tags_length is not UNSET:
            field_dict["tags_length"] = tags_length
        if max_tags_length is not UNSET:
            field_dict["max_tags_length"] = max_tags_length
        if remove_tags is not UNSET:
            field_dict["remove_tags"] = remove_tags
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if limits_url is not UNSET:
            field_dict["limits_url"] = limits_url
        if max_video_bytes is not UNSET:
            field_dict["max_video_bytes"] = max_video_bytes
        if max_image_bytes is not UNSET:
            field_dict["max_image_bytes"] = max_image_bytes
        if parameter is not UNSET:
            field_dict["parameter"] = parameter
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if first_used_at is not UNSET:
            field_dict["first_used_at"] = first_used_at
        if url is not UNSET:
            field_dict["url"] = url
        if field is not UNSET:
            field_dict["field"] = field
        if upstream_status is not UNSET:
            field_dict["upstream_status"] = upstream_status
        if attempts is not UNSET:
            field_dict["attempts"] = attempts
        if ceiling is not UNSET:
            field_dict["ceiling"] = ceiling
        if detected_links is not UNSET:
            field_dict["detected_links"] = detected_links
        if link_used is not UNSET:
            field_dict["link_used"] = link_used
        if link_limit is not UNSET:
            field_dict["link_limit"] = link_limit

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        profiles = cast(list[str], d.pop("profiles", UNSET))

        file_id = d.pop("file_id", UNSET)

        def _parse_progress(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        progress = _parse_progress(d.pop("progress", UNSET))

        retry_after_seconds = d.pop("retry_after_seconds", UNSET)

        upgrade_url = d.pop("upgrade_url", UNSET)

        required = d.pop("required", UNSET)

        platform = d.pop("platform", UNSET)

        plan = d.pop("plan", UNSET)

        used = d.pop("used", UNSET)

        limit = d.pop("limit", UNSET)

        window = d.pop("window", UNSET)

        _resets_at = d.pop("resets_at", UNSET)
        resets_at: datetime.datetime | Unset
        if isinstance(_resets_at, Unset):
            resets_at = UNSET
        else:
            resets_at = datetime.datetime.fromisoformat(_resets_at)

        trial_available = d.pop("trial_available", UNSET)

        reason = d.pop("reason", UNSET)

        scheduled_for = d.pop("scheduled_for", UNSET)

        status = d.pop("status", UNSET)

        tags_length = d.pop("tags_length", UNSET)

        max_tags_length = d.pop("max_tags_length", UNSET)

        remove_tags = d.pop("remove_tags", UNSET)

        size_bytes = d.pop("size_bytes", UNSET)

        limits_url = d.pop("limits_url", UNSET)

        def _parse_max_video_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_video_bytes = _parse_max_video_bytes(d.pop("max_video_bytes", UNSET))

        def _parse_max_image_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_image_bytes = _parse_max_image_bytes(d.pop("max_image_bytes", UNSET))

        parameter = d.pop("parameter", UNSET)

        started_at = d.pop("started_at", UNSET)

        first_used_at = d.pop("first_used_at", UNSET)

        url = d.pop("url", UNSET)

        field = d.pop("field", UNSET)

        upstream_status = d.pop("upstream_status", UNSET)

        attempts = d.pop("attempts", UNSET)

        ceiling = d.pop("ceiling", UNSET)

        detected_links = cast(list[str], d.pop("detected_links", UNSET))

        link_used = d.pop("link_used", UNSET)

        link_limit = d.pop("link_limit", UNSET)

        error_object = cls(
            code=code,
            message=message,
            profiles=profiles,
            file_id=file_id,
            progress=progress,
            retry_after_seconds=retry_after_seconds,
            upgrade_url=upgrade_url,
            required=required,
            platform=platform,
            plan=plan,
            used=used,
            limit=limit,
            window=window,
            resets_at=resets_at,
            trial_available=trial_available,
            reason=reason,
            scheduled_for=scheduled_for,
            status=status,
            tags_length=tags_length,
            max_tags_length=max_tags_length,
            remove_tags=remove_tags,
            size_bytes=size_bytes,
            limits_url=limits_url,
            max_video_bytes=max_video_bytes,
            max_image_bytes=max_image_bytes,
            parameter=parameter,
            started_at=started_at,
            first_used_at=first_used_at,
            url=url,
            field=field,
            upstream_status=upstream_status,
            attempts=attempts,
            ceiling=ceiling,
            detected_links=detected_links,
            link_used=link_used,
            link_limit=link_limit,
        )

        error_object.additional_properties = d
        return error_object

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
