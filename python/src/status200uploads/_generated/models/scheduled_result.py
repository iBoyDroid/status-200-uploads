from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.warning import Warning_


T = TypeVar("T", bound="ScheduledResult")


@_attrs_define
class ScheduledResult:
    """
    Attributes:
        platform (str):
        post_id (None | str): That network's History id, when there is one.
        status (str):
        done (bool):
        publish_id (None | str):
        permalink (None | str):
        error_message (None | str): Why it failed or was not sent.
        notices (list[Warning_]): That network's post's notices (see PostItem): what we changed to get a TikTok photo
            post out, for example a photo sent as a smaller copy, and moved_to_next_day on any network (another network of
            this scheduled post moved to the next day as a scheduled post of its own). Empty on the other networks when
            nothing moved, and while there is no post (pending, not_sent).
    """

    platform: str
    post_id: None | str
    status: str
    done: bool
    publish_id: None | str
    permalink: None | str
    error_message: None | str
    notices: list[Warning_]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        platform = self.platform

        post_id: None | str
        post_id = self.post_id

        status = self.status

        done = self.done

        publish_id: None | str
        publish_id = self.publish_id

        permalink: None | str
        permalink = self.permalink

        error_message: None | str
        error_message = self.error_message

        notices = []
        for notices_item_data in self.notices:
            notices_item = notices_item_data.to_dict()
            notices.append(notices_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "platform": platform,
                "post_id": post_id,
                "status": status,
                "done": done,
                "publish_id": publish_id,
                "permalink": permalink,
                "error_message": error_message,
                "notices": notices,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.warning import Warning_

        d = dict(src_dict)
        platform = d.pop("platform")

        def _parse_post_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        post_id = _parse_post_id(d.pop("post_id"))

        status = d.pop("status")

        done = d.pop("done")

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

        notices = []
        _notices = d.pop("notices")
        for notices_item_data in _notices:
            notices_item = Warning_.from_dict(notices_item_data)

            notices.append(notices_item)

        scheduled_result = cls(
            platform=platform,
            post_id=post_id,
            status=status,
            done=done,
            publish_id=publish_id,
            permalink=permalink,
            error_message=error_message,
            notices=notices,
        )

        scheduled_result.additional_properties = d
        return scheduled_result

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
