from typing import Literal

UploadLinkRequestShell = Literal["powershell", "sh"]

UPLOAD_LINK_REQUEST_SHELL_VALUES: set[UploadLinkRequestShell] = {
    "powershell",
    "sh",
}


def check_upload_link_request_shell(value: str) -> UploadLinkRequestShell:
    if value in UPLOAD_LINK_REQUEST_SHELL_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UPLOAD_LINK_REQUEST_SHELL_VALUES!r}"
    )
