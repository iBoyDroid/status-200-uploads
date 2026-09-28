from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_object import ErrorObject
    from ..models.status_200_ids import Status200Ids


T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """
    Attributes:
        error (ErrorObject): REST refusals carry code, message and, for a plan refusal, upgrade_url, plus the facts of
            the refusal below. They carry no next_step and no retry field (those are the AI connector's); what a client may
            send again is components.x-status200-retry.
        status200 (Status200Ids | Unset): Our ids, on every answer (any status) that recorded a post in History or a
            scheduled post; never on a dry run or on a refusal that recorded nothing. Use it rather than data.post_id, which
            is the network's own id on Facebook, LinkedIn and Skool.
    """

    error: ErrorObject
    status200: Status200Ids | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        status200: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status200, Unset):
            status200 = self.status200.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
            }
        )
        if status200 is not UNSET:
            field_dict["status200"] = status200

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.error_object import ErrorObject
        from ..models.status_200_ids import Status200Ids

        d = dict(src_dict)
        error = ErrorObject.from_dict(d.pop("error"))

        _status200 = d.pop("status200", UNSET)
        status200: Status200Ids | Unset
        if isinstance(_status200, Unset):
            status200 = UNSET
        else:
            status200 = Status200Ids.from_dict(_status200)

        error_response = cls(
            error=error,
            status200=status200,
        )

        error_response.additional_properties = d
        return error_response

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
