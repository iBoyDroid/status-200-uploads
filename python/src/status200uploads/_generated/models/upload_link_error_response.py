from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.upload_link_error import UploadLinkError


T = TypeVar("T", bound="UploadLinkErrorResponse")


@_attrs_define
class UploadLinkErrorResponse:
    """
    Attributes:
        error (UploadLinkError): The refusals of the upload-link endpoints. Besides the fields here they carry next_step
            (what to do next, in a sentence) and, for most codes, retry: "never" (the same request cannot succeed now) or
            "after_reset" (a budget that frees at 00:00 UTC). The AI connector reads the same answers; what a client may
            send again is components.x-status200-retry.
    """

    error: UploadLinkError
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.upload_link_error import UploadLinkError

        d = dict(src_dict)
        error = UploadLinkError.from_dict(d.pop("error"))

        upload_link_error_response = cls(
            error=error,
        )

        upload_link_error_response.additional_properties = d
        return upload_link_error_response

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
