from typing import Literal

UploadLinkRequestRunner = Literal["native", "node"]

UPLOAD_LINK_REQUEST_RUNNER_VALUES: set[UploadLinkRequestRunner] = {
    "native",
    "node",
}


def check_upload_link_request_runner(value: str) -> UploadLinkRequestRunner:
    if value in UPLOAD_LINK_REQUEST_RUNNER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UPLOAD_LINK_REQUEST_RUNNER_VALUES!r}"
    )
