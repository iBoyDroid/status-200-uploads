from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_item_kind import PostItemKind, check_post_item_kind

if TYPE_CHECKING:
    from ..models.figures import Figures


T = TypeVar("T", bound="PostReadDataType0")


@_attrs_define
class PostReadDataType0:
    """
    Attributes:
        id (UUID):
        kind (PostItemKind):
        profile_id (None | str):
        platform (str):
        status (str): timeout = sent, never confirmed; do not send it again.
        done (bool): True once it will not change by itself.
        media_type (None | str):
        publish_id (None | str): The network's own id.
        permalink (None | str):
        error_message (None | str):
        at (datetime.datetime | None):
        updated_at (datetime.datetime | None):
        scheduled_post_id (None | str):
        figures (Figures | None): null unless the post succeeded.
    """

    id: UUID
    kind: PostItemKind
    profile_id: None | str
    platform: str
    status: str
    done: bool
    media_type: None | str
    publish_id: None | str
    permalink: None | str
    error_message: None | str
    at: datetime.datetime | None
    updated_at: datetime.datetime | None
    scheduled_post_id: None | str
    figures: Figures | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.figures import Figures

        id = str(self.id)

        kind: str = self.kind

        profile_id: None | str
        profile_id = self.profile_id

        platform = self.platform

        status = self.status

        done = self.done

        media_type: None | str
        media_type = self.media_type

        publish_id: None | str
        publish_id = self.publish_id

        permalink: None | str
        permalink = self.permalink

        error_message: None | str
        error_message = self.error_message

        at: None | str
        if isinstance(self.at, datetime.datetime):
            at = self.at.isoformat()
        else:
            at = self.at

        updated_at: None | str
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        scheduled_post_id: None | str
        scheduled_post_id = self.scheduled_post_id

        figures: dict[str, Any] | None
        if isinstance(self.figures, Figures):
            figures = self.figures.to_dict()
        else:
            figures = self.figures

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "profile_id": profile_id,
                "platform": platform,
                "status": status,
                "done": done,
                "media_type": media_type,
                "publish_id": publish_id,
                "permalink": permalink,
                "error_message": error_message,
                "at": at,
                "updated_at": updated_at,
                "scheduled_post_id": scheduled_post_id,
                "figures": figures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.figures import Figures

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        kind = check_post_item_kind(d.pop("kind"))

        def _parse_profile_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profile_id = _parse_profile_id(d.pop("profile_id"))

        platform = d.pop("platform")

        status = d.pop("status")

        done = d.pop("done")

        def _parse_media_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        media_type = _parse_media_type(d.pop("media_type"))

        def _parse_publish_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        publish_id = _parse_publish_id(d.pop("publish_id"))

        def _parse_permalink(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        permalink = _parse_permalink(d.pop("permalink"))

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("error_message"))

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

        def _parse_scheduled_post_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        scheduled_post_id = _parse_scheduled_post_id(d.pop("scheduled_post_id"))

        def _parse_figures(data: object) -> Figures | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                figures_type_1 = Figures.from_dict(data)

                return figures_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Figures | None, data)

        figures = _parse_figures(d.pop("figures"))

        post_read_data_type_0 = cls(
            id=id,
            kind=kind,
            profile_id=profile_id,
            platform=platform,
            status=status,
            done=done,
            media_type=media_type,
            publish_id=publish_id,
            permalink=permalink,
            error_message=error_message,
            at=at,
            updated_at=updated_at,
            scheduled_post_id=scheduled_post_id,
            figures=figures,
        )

        post_read_data_type_0.additional_properties = d
        return post_read_data_type_0

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
