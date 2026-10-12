from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.photo_size import PhotoSize


T = TypeVar("T", bound="Warning_")


@_attrs_define
class Warning_:
    """Something the caller should know about a request that went through. The post was still sent. resized_for_tiktok (a
    TikTok photo larger than 1080 x 1920 sent as a smaller copy) also carries size (the photo, as it is shown) and
    copy_size (what TikTok got); see https://status200uploads.com/docs/api#tiktok-photos.

        Attributes:
            code (str):
            message (str):
            field (str | Unset): Where the field sits in the request, e.g. post.youtube.allowEmbedding.
            did_you_mean (str | Unset):
            photo (int | Unset): converted_to_jpeg and resized_for_tiktok - which photo of the post, counting from 1.
            photos (int | Unset): resized_for_tiktok - how many photos the post has.
            from_ (str | Unset): converted_to_jpeg and resized_for_tiktok - the photo's own format.
            size (PhotoSize | Unset): A photo's size in pixels, as the photo is shown (after its EXIF orientation).
            copy_size (PhotoSize | Unset): A photo's size in pixels, as the photo is shown (after its EXIF orientation).
    """

    code: str
    message: str
    field: str | Unset = UNSET
    did_you_mean: str | Unset = UNSET
    photo: int | Unset = UNSET
    photos: int | Unset = UNSET
    from_: str | Unset = UNSET
    size: PhotoSize | Unset = UNSET
    copy_size: PhotoSize | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        field = self.field

        did_you_mean = self.did_you_mean

        photo = self.photo

        photos = self.photos

        from_ = self.from_

        size: dict[str, Any] | Unset = UNSET
        if not isinstance(self.size, Unset):
            size = self.size.to_dict()

        copy_size: dict[str, Any] | Unset = UNSET
        if not isinstance(self.copy_size, Unset):
            copy_size = self.copy_size.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if field is not UNSET:
            field_dict["field"] = field
        if did_you_mean is not UNSET:
            field_dict["did_you_mean"] = did_you_mean
        if photo is not UNSET:
            field_dict["photo"] = photo
        if photos is not UNSET:
            field_dict["photos"] = photos
        if from_ is not UNSET:
            field_dict["from"] = from_
        if size is not UNSET:
            field_dict["size"] = size
        if copy_size is not UNSET:
            field_dict["copy_size"] = copy_size

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.photo_size import PhotoSize

        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        field = d.pop("field", UNSET)

        did_you_mean = d.pop("did_you_mean", UNSET)

        photo = d.pop("photo", UNSET)

        photos = d.pop("photos", UNSET)

        from_ = d.pop("from", UNSET)

        _size = d.pop("size", UNSET)
        size: PhotoSize | Unset
        if isinstance(_size, Unset):
            size = UNSET
        else:
            size = PhotoSize.from_dict(_size)

        _copy_size = d.pop("copy_size", UNSET)
        copy_size: PhotoSize | Unset
        if isinstance(_copy_size, Unset):
            copy_size = UNSET
        else:
            copy_size = PhotoSize.from_dict(_copy_size)

        warning = cls(
            code=code,
            message=message,
            field=field,
            did_you_mean=did_you_mean,
            photo=photo,
            photos=photos,
            from_=from_,
            size=size,
            copy_size=copy_size,
        )

        warning.additional_properties = d
        return warning

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
