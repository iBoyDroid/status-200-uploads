from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.upload_link_upload import UploadLinkUpload
    from ..models.upload_link_uploader import UploadLinkUploader


T = TypeVar("T", bound="UploadLink")


@_attrs_define
class UploadLink:
    """The answer also carries next_step: how to run the command (or send the file), the timeout, and what to call when it
    ends.

        Attributes:
            success (bool):
            file_id (UUID): The id of this upload, and of the file in the media library once it is ready (send it in
                post.content.mediaID).
            status (str):
            file_name (str): The name that is kept (folders and control characters removed, at most 120 characters).
            size (int):
            type_ (str): Decided by the extension (an .m4v file is video/mp4).
            sha256 (str): Lower case.
            renewed (bool): true for a fresh token for the same address (POST /media/uploads/{file_id}/token, or the same
                file asked for again from the same key).
            upload (UploadLinkUpload):
            uploader (UploadLinkUploader | Unset): Only when shell was sent.
    """

    success: bool
    file_id: UUID
    status: str
    file_name: str
    size: int
    type_: str
    sha256: str
    renewed: bool
    upload: UploadLinkUpload
    uploader: UploadLinkUploader | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        file_id = str(self.file_id)

        status = self.status

        file_name = self.file_name

        size = self.size

        type_ = self.type_

        sha256 = self.sha256

        renewed = self.renewed

        upload = self.upload.to_dict()

        uploader: dict[str, Any] | Unset = UNSET
        if not isinstance(self.uploader, Unset):
            uploader = self.uploader.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "file_id": file_id,
                "status": status,
                "file_name": file_name,
                "size": size,
                "type": type_,
                "sha256": sha256,
                "renewed": renewed,
                "upload": upload,
            }
        )
        if uploader is not UNSET:
            field_dict["uploader"] = uploader

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.upload_link_upload import UploadLinkUpload
        from ..models.upload_link_uploader import UploadLinkUploader

        d = dict(src_dict)
        success = d.pop("success")

        file_id = UUID(d.pop("file_id"))

        status = d.pop("status")

        file_name = d.pop("file_name")

        size = d.pop("size")

        type_ = d.pop("type")

        sha256 = d.pop("sha256")

        renewed = d.pop("renewed")

        upload = UploadLinkUpload.from_dict(d.pop("upload"))

        _uploader = d.pop("uploader", UNSET)
        uploader: UploadLinkUploader | Unset
        if isinstance(_uploader, Unset):
            uploader = UNSET
        else:
            uploader = UploadLinkUploader.from_dict(_uploader)

        upload_link = cls(
            success=success,
            file_id=file_id,
            status=status,
            file_name=file_name,
            size=size,
            type_=type_,
            sha256=sha256,
            renewed=renewed,
            upload=upload,
            uploader=uploader,
        )

        upload_link.additional_properties = d
        return upload_link

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
