from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Status200Ids")


@_attrs_define
class Status200Ids:
    """Our ids, on every answer (any status) that recorded a post in History or a scheduled post; never on a dry run or on
    a refusal that recorded nothing. Use it rather than data.post_id, which is the network's own id on Facebook,
    LinkedIn and Skool.

        Attributes:
            post_id (None | UUID): Our History id.
            scheduled_post_id (None | UUID):
            status_url (str): GET https://status200uploads.com/api/v2/posts/<post_id, else scheduled_post_id>.
    """

    post_id: None | UUID
    scheduled_post_id: None | UUID
    status_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post_id: None | str
        if isinstance(self.post_id, UUID):
            post_id = str(self.post_id)
        else:
            post_id = self.post_id

        scheduled_post_id: None | str
        if isinstance(self.scheduled_post_id, UUID):
            scheduled_post_id = str(self.scheduled_post_id)
        else:
            scheduled_post_id = self.scheduled_post_id

        status_url = self.status_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "post_id": post_id,
                "scheduled_post_id": scheduled_post_id,
                "status_url": status_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_post_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                post_id_type_0 = UUID(data)

                return post_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        post_id = _parse_post_id(d.pop("post_id"))

        def _parse_scheduled_post_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scheduled_post_id_type_0 = UUID(data)

                return scheduled_post_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        scheduled_post_id = _parse_scheduled_post_id(d.pop("scheduled_post_id"))

        status_url = d.pop("status_url")

        status_200_ids = cls(
            post_id=post_id,
            scheduled_post_id=scheduled_post_id,
            status_url=status_url,
        )

        status_200_ids.additional_properties = d
        return status_200_ids

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
