from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scheduled_post_item_kind import ScheduledPostItemKind, check_scheduled_post_item_kind

if TYPE_CHECKING:
    from ..models.scheduled_result import ScheduledResult


T = TypeVar("T", bound="PostReadDataType1")


@_attrs_define
class PostReadDataType1:
    """
    Attributes:
        id (UUID):
        kind (ScheduledPostItemKind):
        profile_id (None | str):
        platforms (list[str]):
        status (str):
        outcome (str):
        done (bool):
        media_type (None | str):
        at (datetime.datetime | None):
        scheduled_for (datetime.datetime | None):
        created_at (datetime.datetime | None):
        updated_at (datetime.datetime | None):
        note (None | str): While it waits, why it moved (for example a used-up daily allowance). Not an error.
        error_message (None | str):
        results (list[ScheduledResult]):
    """

    id: UUID
    kind: ScheduledPostItemKind
    profile_id: None | str
    platforms: list[str]
    status: str
    outcome: str
    done: bool
    media_type: None | str
    at: datetime.datetime | None
    scheduled_for: datetime.datetime | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    note: None | str
    error_message: None | str
    results: list[ScheduledResult]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        kind: str = self.kind

        profile_id: None | str
        profile_id = self.profile_id

        platforms = self.platforms

        status = self.status

        outcome = self.outcome

        done = self.done

        media_type: None | str
        media_type = self.media_type

        at: None | str
        if isinstance(self.at, datetime.datetime):
            at = self.at.isoformat()
        else:
            at = self.at

        scheduled_for: None | str
        if isinstance(self.scheduled_for, datetime.datetime):
            scheduled_for = self.scheduled_for.isoformat()
        else:
            scheduled_for = self.scheduled_for

        created_at: None | str
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        note: None | str
        note = self.note

        error_message: None | str
        error_message = self.error_message

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "profile_id": profile_id,
                "platforms": platforms,
                "status": status,
                "outcome": outcome,
                "done": done,
                "media_type": media_type,
                "at": at,
                "scheduled_for": scheduled_for,
                "created_at": created_at,
                "updated_at": updated_at,
                "note": note,
                "error_message": error_message,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.scheduled_result import ScheduledResult

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        kind = check_scheduled_post_item_kind(d.pop("kind"))

        def _parse_profile_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profile_id = _parse_profile_id(d.pop("profile_id"))

        platforms = cast(list[str], d.pop("platforms"))

        status = d.pop("status")

        outcome = d.pop("outcome")

        done = d.pop("done")

        def _parse_media_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        media_type = _parse_media_type(d.pop("media_type"))

        def _parse_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                at_type_0 = datetime.datetime.fromisoformat(data)

                return at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        at = _parse_at(d.pop("at"))

        def _parse_scheduled_for(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scheduled_for_type_0 = datetime.datetime.fromisoformat(data)

                return scheduled_for_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        scheduled_for = _parse_scheduled_for(d.pop("scheduled_for"))

        def _parse_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        created_at = _parse_created_at(d.pop("created_at"))

        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updated_at"))

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("error_message"))

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = ScheduledResult.from_dict(results_item_data)

            results.append(results_item)

        post_read_data_type_1 = cls(
            id=id,
            kind=kind,
            profile_id=profile_id,
            platforms=platforms,
            status=status,
            outcome=outcome,
            done=done,
            media_type=media_type,
            at=at,
            scheduled_for=scheduled_for,
            created_at=created_at,
            updated_at=updated_at,
            note=note,
            error_message=error_message,
            results=results,
        )

        post_read_data_type_1.additional_properties = d
        return post_read_data_type_1

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
