from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.you_tube_options_license import YouTubeOptionsLicense, check_you_tube_options_license
from ..models.you_tube_options_privacy_status import (
    YouTubeOptionsPrivacyStatus,
    check_you_tube_options_privacy_status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="YouTubeOptions")


@_attrs_define
class YouTubeOptions:
    """
    Attributes:
        title (str | Unset): The video title, up to 100 characters (longer is shortened at the end of a word). Without
            it the title comes from content.text.
        description (str | Unset): The description, up to 5,000 bytes. Without it, content.text when a title was sent.
        privacy_status (YouTubeOptionsPrivacyStatus | Unset):  Default: 'private'.
        tags (list[str] | Unset): YouTube allows 500 characters of tags counted its own way; a longer list is 400
            youtube_tags_too_long before the upload.
        category_id (str | Unset):  Default: '22'.
        made_for_kids (bool | Unset):  Default: False.
        embeddable (bool | Unset):  Default: True.
        license_ (YouTubeOptionsLicense | Unset):  Default: 'youtube'.
        public_stats_viewable (bool | Unset):  Default: True.
        notify_subscribers (bool | Unset):  Default: True.
        default_language (str | Unset): The language of the title and description (en, es, fr ...).
    """

    title: str | Unset = UNSET
    description: str | Unset = UNSET
    privacy_status: YouTubeOptionsPrivacyStatus | Unset = "private"
    tags: list[str] | Unset = UNSET
    category_id: str | Unset = "22"
    made_for_kids: bool | Unset = False
    embeddable: bool | Unset = True
    license_: YouTubeOptionsLicense | Unset = "youtube"
    public_stats_viewable: bool | Unset = True
    notify_subscribers: bool | Unset = True
    default_language: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        privacy_status: str | Unset = UNSET
        if not isinstance(self.privacy_status, Unset):
            privacy_status = self.privacy_status

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        category_id = self.category_id

        made_for_kids = self.made_for_kids

        embeddable = self.embeddable

        license_: str | Unset = UNSET
        if not isinstance(self.license_, Unset):
            license_ = self.license_

        public_stats_viewable = self.public_stats_viewable

        notify_subscribers = self.notify_subscribers

        default_language = self.default_language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if privacy_status is not UNSET:
            field_dict["privacyStatus"] = privacy_status
        if tags is not UNSET:
            field_dict["tags"] = tags
        if category_id is not UNSET:
            field_dict["categoryId"] = category_id
        if made_for_kids is not UNSET:
            field_dict["madeForKids"] = made_for_kids
        if embeddable is not UNSET:
            field_dict["embeddable"] = embeddable
        if license_ is not UNSET:
            field_dict["license"] = license_
        if public_stats_viewable is not UNSET:
            field_dict["publicStatsViewable"] = public_stats_viewable
        if notify_subscribers is not UNSET:
            field_dict["notifySubscribers"] = notify_subscribers
        if default_language is not UNSET:
            field_dict["defaultLanguage"] = default_language

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        _privacy_status = d.pop("privacyStatus", UNSET)
        privacy_status: YouTubeOptionsPrivacyStatus | Unset
        if isinstance(_privacy_status, Unset):
            privacy_status = UNSET
        else:
            privacy_status = check_you_tube_options_privacy_status(_privacy_status)

        tags = cast(list[str], d.pop("tags", UNSET))

        category_id = d.pop("categoryId", UNSET)

        made_for_kids = d.pop("madeForKids", UNSET)

        embeddable = d.pop("embeddable", UNSET)

        _license_ = d.pop("license", UNSET)
        license_: YouTubeOptionsLicense | Unset
        if isinstance(_license_, Unset):
            license_ = UNSET
        else:
            license_ = check_you_tube_options_license(_license_)

        public_stats_viewable = d.pop("publicStatsViewable", UNSET)

        notify_subscribers = d.pop("notifySubscribers", UNSET)

        default_language = d.pop("defaultLanguage", UNSET)

        you_tube_options = cls(
            title=title,
            description=description,
            privacy_status=privacy_status,
            tags=tags,
            category_id=category_id,
            made_for_kids=made_for_kids,
            embeddable=embeddable,
            license_=license_,
            public_stats_viewable=public_stats_viewable,
            notify_subscribers=notify_subscribers,
            default_language=default_language,
        )

        you_tube_options.additional_properties = d
        return you_tube_options

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
