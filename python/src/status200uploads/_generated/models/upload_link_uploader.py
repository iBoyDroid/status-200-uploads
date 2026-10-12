from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadLinkUploader")


@_attrs_define
class UploadLinkUploader:
    """Only when shell was sent.

    Attributes:
        shell (str):
        runner (str):
        version (str): The uploader version. A published version never changes; a new uploader is a new version.
        download_url (str): Where the command downloads the uploader from (served as text/plain).
        sha256 (str): The SHA-256 of that file. The command refuses to run a download with any other.
        max_run_seconds (int):
        command (str): Run it as it is in that shell (never inside another shell), with <PATH> in its S200_FILE line
            replaced by the file's full path, and with a timeout of at least max_run_seconds + 60 seconds. It downloads the
            uploader into a fresh folder, checks its SHA-256, sends the file and removes the folder. Its exit code is the
            uploader's: 0 done, 1 failed, 2 refused, 3 partial, 4 token_rejected, 5 busy, 6 bad_command. It also ends with
            1, with a message and no JSON line, when it stops before the uploader runs: the download failed (run it once
            more), the download's SHA-256 did not match (stop), or Node.js or Windows PowerShell is missing (ask again with
            the runner or shell its message names).
    """

    shell: str
    runner: str
    version: str
    download_url: str
    sha256: str
    max_run_seconds: int
    command: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shell = self.shell

        runner = self.runner

        version = self.version

        download_url = self.download_url

        sha256 = self.sha256

        max_run_seconds = self.max_run_seconds

        command = self.command

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shell": shell,
                "runner": runner,
                "version": version,
                "download_url": download_url,
                "sha256": sha256,
                "max_run_seconds": max_run_seconds,
                "command": command,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        shell = d.pop("shell")

        runner = d.pop("runner")

        version = d.pop("version")

        download_url = d.pop("download_url")

        sha256 = d.pop("sha256")

        max_run_seconds = d.pop("max_run_seconds")

        command = d.pop("command")

        upload_link_uploader = cls(
            shell=shell,
            runner=runner,
            version=version,
            download_url=download_url,
            sha256=sha256,
            max_run_seconds=max_run_seconds,
            command=command,
        )

        upload_link_uploader.additional_properties = d
        return upload_link_uploader

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
