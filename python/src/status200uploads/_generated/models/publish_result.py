from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_result_data import PublishResultData
    from ..models.status_200_ids import Status200Ids
    from ..models.warning import Warning_


T = TypeVar("T", bound="PublishResult")


@_attrs_define
class PublishResult:
    """
    Attributes:
        data (PublishResultData): The network's result. TikTok {status "processing", post_id (ours), publish_id,
            message}; Instagram {status "processing", post_id (ours), container_id, message}; X {tweet_id, text, url};
            LinkedIn {post_id (LinkedIn's), url}; Pinterest {pin_id, url, title, board_id}; Threads {thread_id, permalink};
            Skool {post_id (Skool's), url}; Facebook Graph's own {id, post_id?, video_id?, permalink?}; YouTube youtube-
            api's {video_id, url}.
        warnings (list[Warning_] | Unset):
        status200 (Status200Ids | Unset): Our ids, on every answer (any status) that recorded a post in History or a
            scheduled post; never on a dry run or on a refusal that recorded nothing. Use it rather than data.post_id, which
            is the network's own id on Facebook, LinkedIn and Skool.
    """

    data: PublishResultData
    warnings: list[Warning_] | Unset = UNSET
    status200: Status200Ids | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

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
        field_dict.update(
            {
                "data": data,
            }
        )
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if status200 is not UNSET:
            field_dict["status200"] = status200

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.publish_result_data import PublishResultData
        from ..models.status_200_ids import Status200Ids
        from ..models.warning import Warning_

        d = dict(src_dict)
        data = PublishResultData.from_dict(d.pop("data"))

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

        publish_result = cls(
            data=data,
            warnings=warnings,
            status200=status200,
        )

        publish_result.additional_properties = d
        return publish_result

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
