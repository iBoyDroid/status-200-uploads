from typing import Literal

UploadTokenRequestShell = Literal["powershell", "sh"]

UPLOAD_TOKEN_REQUEST_SHELL_VALUES: set[UploadTokenRequestShell] = {
    "powershell",
    "sh",
}


def check_upload_token_request_shell(value: str) -> UploadTokenRequestShell:
    if value in UPLOAD_TOKEN_REQUEST_SHELL_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UPLOAD_TOKEN_REQUEST_SHELL_VALUES!r}"
    )
