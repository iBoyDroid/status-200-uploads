from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CancelResultData")


@_attrs_define
class CancelResultData:
    """
    Attributes:
        scheduled_post_id (UUID):
        status (str):
        platforms (list[str]):
        was_due_at (str): When it was due (its scheduled_at).
        message (str):
        already_cancelled (bool | Unset): Present (true) when it was cancelled before this request. Nothing changed.
    """

    scheduled_post_id: UUID
    status: str
    platforms: list[str]
    was_due_at: str
    message: str
    already_cancelled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scheduled_post_id = str(self.scheduled_post_id)

        status = self.status

        platforms = self.platforms

        was_due_at = self.was_due_at

        message = self.message

        already_cancelled = self.already_cancelled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scheduled_post_id": scheduled_post_id,
                "status": status,
                "platforms": platforms,
                "was_due_at": was_due_at,
                "message": message,
            }
        )
        if already_cancelled is not UNSET:
            field_dict["already_cancelled"] = already_cancelled

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        scheduled_post_id = UUID(d.pop("scheduled_post_id"))

        status = d.pop("status")

        platforms = cast(list[str], d.pop("platforms"))

        was_due_at = d.pop("was_due_at")

        message = d.pop("message")

        already_cancelled = d.pop("already_cancelled", UNSET)

        cancel_result_data = cls(
            scheduled_post_id=scheduled_post_id,
            status=status,
            platforms=platforms,
            was_due_at=was_due_at,
            message=message,
            already_cancelled=already_cancelled,
        )

        cancel_result_data.additional_properties = d
        return cancel_result_data

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
