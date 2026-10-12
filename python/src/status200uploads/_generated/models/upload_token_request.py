from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.upload_token_request_runner import (
    UploadTokenRequestRunner,
    check_upload_token_request_runner,
)
from ..models.upload_token_request_shell import (
    UploadTokenRequestShell,
    check_upload_token_request_shell,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadTokenRequest")


@_attrs_define
class UploadTokenRequest:
    """Optional. The file's name, size and SHA-256 are the link's own and are not sent again.

    Attributes:
        shell (UploadTokenRequestShell | Unset): As for a new link; with it the answer carries a new uploader.command.
        runner (UploadTokenRequestRunner | Unset):  Default: 'native'.
        max_run_seconds (int | Unset):  Default: 100.
    """

    shell: UploadTokenRequestShell | Unset = UNSET
    runner: UploadTokenRequestRunner | Unset = "native"
    max_run_seconds: int | Unset = 100
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shell: str | Unset = UNSET
        if not isinstance(self.shell, Unset):
            shell = self.shell

        runner: str | Unset = UNSET
        if not isinstance(self.runner, Unset):
            runner = self.runner

        max_run_seconds = self.max_run_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if shell is not UNSET:
            field_dict["shell"] = shell
        if runner is not UNSET:
            field_dict["runner"] = runner
        if max_run_seconds is not UNSET:
            field_dict["max_run_seconds"] = max_run_seconds

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _shell = d.pop("shell", UNSET)
        shell: UploadTokenRequestShell | Unset
        if isinstance(_shell, Unset):
            shell = UNSET
        else:
            shell = check_upload_token_request_shell(_shell)

        _runner = d.pop("runner", UNSET)
        runner: UploadTokenRequestRunner | Unset
        if isinstance(_runner, Unset):
            runner = UNSET
        else:
            runner = check_upload_token_request_runner(_runner)

        max_run_seconds = d.pop("max_run_seconds", UNSET)

        upload_token_request = cls(
            shell=shell,
            runner=runner,
            max_run_seconds=max_run_seconds,
        )

        upload_token_request.additional_properties = d
        return upload_token_request

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
