from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.upload_link_request_runner import (
    UploadLinkRequestRunner,
    check_upload_link_request_runner,
)
from ..models.upload_link_request_shell import (
    UploadLinkRequestShell,
    check_upload_link_request_shell,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadLinkRequest")


@_attrs_define
class UploadLinkRequest:
    """file_id is not part of a new link (400): a fresh token for an unfinished upload is POST
    /media/uploads/{file_id}/token. Other fields are not read.

        Attributes:
            file_name (str): The file's name, for example EP01.mp4 (a path works: folders are cut off and never stored). Its
                extension decides the type: .mp4 and .m4v (stored as MP4), .mov, .webm, .jpg and .jpeg, .png, .webp; anything
                else is 415. Control and format characters are removed, and a name over 120 characters is shortened with its
                extension kept.
            size_bytes (int): The file's exact size in bytes: videos up to 5 GB (5,368,709,120 bytes), images up to 20 MB
                (20,971,520 bytes); larger is 413. The file that arrives must be exactly this size.
            sha256 (str): The file's SHA-256: 64 hex characters, either case (Windows PowerShell's Get-FileHash prints upper
                case). The file that arrives must have exactly this hash.
            shell (UploadLinkRequestShell | Unset): For a ready-made command in the answer (uploader.command): powershell
                for Windows PowerShell, sh for sh, bash or zsh (macOS, Linux, WSL and Git Bash). Without it the answer has no
                uploader block: send the file with your own TUS client.
            runner (UploadLinkRequestRunner | Unset): native runs our PowerShell or sh uploader; node runs our Node.js
                uploader (Node.js 18 or newer). Default: 'native'.
            max_run_seconds (int | Unset): How long one run of the uploader may take; it always ends within that plus 10
                seconds, so give the command a timeout at least 60 seconds longer. A run that used its time ends with exit 3
                (partial), and the same command continues where it stopped. Default: 100.
    """

    file_name: str
    size_bytes: int
    sha256: str
    shell: UploadLinkRequestShell | Unset = UNSET
    runner: UploadLinkRequestRunner | Unset = "native"
    max_run_seconds: int | Unset = 100
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_name = self.file_name

        size_bytes = self.size_bytes

        sha256 = self.sha256

        shell: str | Unset = UNSET
        if not isinstance(self.shell, Unset):
            shell = self.shell

        runner: str | Unset = UNSET
        if not isinstance(self.runner, Unset):
            runner = self.runner

        max_run_seconds = self.max_run_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_name": file_name,
                "size_bytes": size_bytes,
                "sha256": sha256,
            }
        )
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
        file_name = d.pop("file_name")

        size_bytes = d.pop("size_bytes")

        sha256 = d.pop("sha256")

        _shell = d.pop("shell", UNSET)
        shell: UploadLinkRequestShell | Unset
        if isinstance(_shell, Unset):
            shell = UNSET
        else:
            shell = check_upload_link_request_shell(_shell)

        _runner = d.pop("runner", UNSET)
        runner: UploadLinkRequestRunner | Unset
        if isinstance(_runner, Unset):
            runner = UNSET
        else:
            runner = check_upload_link_request_runner(_runner)

        max_run_seconds = d.pop("max_run_seconds", UNSET)

        upload_link_request = cls(
            file_name=file_name,
            size_bytes=size_bytes,
            sha256=sha256,
            shell=shell,
            runner=runner,
            max_run_seconds=max_run_seconds,
        )

        upload_link_request.additional_properties = d
        return upload_link_request

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
