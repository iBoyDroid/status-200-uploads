from typing import Literal

UploadTokenRequestRunner = Literal["native", "node"]

UPLOAD_TOKEN_REQUEST_RUNNER_VALUES: set[UploadTokenRequestRunner] = {
    "native",
    "node",
}


def check_upload_token_request_runner(value: str) -> UploadTokenRequestRunner:
    if value in UPLOAD_TOKEN_REQUEST_RUNNER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UPLOAD_TOKEN_REQUEST_RUNNER_VALUES!r}"
    )
