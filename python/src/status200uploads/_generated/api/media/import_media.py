from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.media_error import MediaError
from ...models.media_import_ready import MediaImportReady
from ...models.media_import_request import MediaImportRequest
from ...models.media_import_started import MediaImportStarted
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: MediaImportRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/media",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> MediaError | MediaImportReady | MediaImportStarted:
    if response.status_code == 200:
        response_200 = MediaImportReady.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = MediaImportStarted.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = MediaError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = MediaError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = MediaError.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = MediaError.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = MediaError.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = MediaError.from_dict(response.json())

        return response_415

    if response.status_code == 422:
        response_422 = MediaError.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = MediaError.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = MediaError.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = MediaError.from_dict(response.json())

        return response_503

    response_default = MediaError.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MediaError | MediaImportReady | MediaImportStarted]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MediaImportRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[MediaError | MediaImportReady | MediaImportStarted]:
    """Import an image or a video from a URL

     Images up to 20 MB, videos up to 5 GB, of the types the media library takes: JPEG, PNG and WebP
    images, MP4 (M4V too), MOV and WebM videos. The source is probed first: a HEAD, then a ranged GET of
    one byte, or of the first 4 KB when the server sends no type or a generic one such as
    application/octet-stream (or when the HEAD fails), 8 seconds each, so up to about 16 seconds. A file
    without a usable type is judged by those first bytes. The request waits up to about 22 seconds for
    the import: 200 ready, otherwise 202 processing (at once when the declared size cannot finish in
    time). One import every 20 seconds per account. Files are kept for 7 days, and until a scheduled
    post that uses them goes out. A file on a computer, not at a URL: POST /media/uploads.

    Share links (rolling out: switched on account by account, for some accounts first; until then a
    share link is imported exactly as before): where they are on, a Google Drive, Dropbox, OneDrive or
    SharePoint link of a file shared with "Anyone with the link" is turned into the address of the file
    itself and imported like any URL, under the name the provider gives the file, on the paid plans. A
    file the provider gives no name is saved as file.<ext> (for example file.mp4), and a Dropbox file
    without one under the file name in its link. A link that cannot give one file is refused before
    anything is imported (400 with its own code, next_step and provider), and so is a link that needs
    converting sent with a Free key (403 plan_limit_reached); a link that already downloads the file (a
    drive.usercontent.google.com link, a Google Drive uc link with export=download, a OneDrive or
    SharePoint download.aspx?share= link) is imported on every plan, with a Free key exactly as before.
    A refusal decided from the link or the plan does not start the 20-second wait.

    Args:
        idempotency_key (str | Unset):
        body (MediaImportRequest):  Example: {'url': 'https://example.com/video.mp4'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MediaError | MediaImportReady | MediaImportStarted]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: MediaImportRequest,
    idempotency_key: str | Unset = UNSET,
) -> MediaError | MediaImportReady | MediaImportStarted | None:
    """Import an image or a video from a URL

     Images up to 20 MB, videos up to 5 GB, of the types the media library takes: JPEG, PNG and WebP
    images, MP4 (M4V too), MOV and WebM videos. The source is probed first: a HEAD, then a ranged GET of
    one byte, or of the first 4 KB when the server sends no type or a generic one such as
    application/octet-stream (or when the HEAD fails), 8 seconds each, so up to about 16 seconds. A file
    without a usable type is judged by those first bytes. The request waits up to about 22 seconds for
    the import: 200 ready, otherwise 202 processing (at once when the declared size cannot finish in
    time). One import every 20 seconds per account. Files are kept for 7 days, and until a scheduled
    post that uses them goes out. A file on a computer, not at a URL: POST /media/uploads.

    Share links (rolling out: switched on account by account, for some accounts first; until then a
    share link is imported exactly as before): where they are on, a Google Drive, Dropbox, OneDrive or
    SharePoint link of a file shared with "Anyone with the link" is turned into the address of the file
    itself and imported like any URL, under the name the provider gives the file, on the paid plans. A
    file the provider gives no name is saved as file.<ext> (for example file.mp4), and a Dropbox file
    without one under the file name in its link. A link that cannot give one file is refused before
    anything is imported (400 with its own code, next_step and provider), and so is a link that needs
    converting sent with a Free key (403 plan_limit_reached); a link that already downloads the file (a
    drive.usercontent.google.com link, a Google Drive uc link with export=download, a OneDrive or
    SharePoint download.aspx?share= link) is imported on every plan, with a Free key exactly as before.
    A refusal decided from the link or the plan does not start the 20-second wait.

    Args:
        idempotency_key (str | Unset):
        body (MediaImportRequest):  Example: {'url': 'https://example.com/video.mp4'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MediaError | MediaImportReady | MediaImportStarted
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MediaImportRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[MediaError | MediaImportReady | MediaImportStarted]:
    """Import an image or a video from a URL

     Images up to 20 MB, videos up to 5 GB, of the types the media library takes: JPEG, PNG and WebP
    images, MP4 (M4V too), MOV and WebM videos. The source is probed first: a HEAD, then a ranged GET of
    one byte, or of the first 4 KB when the server sends no type or a generic one such as
    application/octet-stream (or when the HEAD fails), 8 seconds each, so up to about 16 seconds. A file
    without a usable type is judged by those first bytes. The request waits up to about 22 seconds for
    the import: 200 ready, otherwise 202 processing (at once when the declared size cannot finish in
    time). One import every 20 seconds per account. Files are kept for 7 days, and until a scheduled
    post that uses them goes out. A file on a computer, not at a URL: POST /media/uploads.

    Share links (rolling out: switched on account by account, for some accounts first; until then a
    share link is imported exactly as before): where they are on, a Google Drive, Dropbox, OneDrive or
    SharePoint link of a file shared with "Anyone with the link" is turned into the address of the file
    itself and imported like any URL, under the name the provider gives the file, on the paid plans. A
    file the provider gives no name is saved as file.<ext> (for example file.mp4), and a Dropbox file
    without one under the file name in its link. A link that cannot give one file is refused before
    anything is imported (400 with its own code, next_step and provider), and so is a link that needs
    converting sent with a Free key (403 plan_limit_reached); a link that already downloads the file (a
    drive.usercontent.google.com link, a Google Drive uc link with export=download, a OneDrive or
    SharePoint download.aspx?share= link) is imported on every plan, with a Free key exactly as before.
    A refusal decided from the link or the plan does not start the 20-second wait.

    Args:
        idempotency_key (str | Unset):
        body (MediaImportRequest):  Example: {'url': 'https://example.com/video.mp4'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MediaError | MediaImportReady | MediaImportStarted]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: MediaImportRequest,
    idempotency_key: str | Unset = UNSET,
) -> MediaError | MediaImportReady | MediaImportStarted | None:
    """Import an image or a video from a URL

     Images up to 20 MB, videos up to 5 GB, of the types the media library takes: JPEG, PNG and WebP
    images, MP4 (M4V too), MOV and WebM videos. The source is probed first: a HEAD, then a ranged GET of
    one byte, or of the first 4 KB when the server sends no type or a generic one such as
    application/octet-stream (or when the HEAD fails), 8 seconds each, so up to about 16 seconds. A file
    without a usable type is judged by those first bytes. The request waits up to about 22 seconds for
    the import: 200 ready, otherwise 202 processing (at once when the declared size cannot finish in
    time). One import every 20 seconds per account. Files are kept for 7 days, and until a scheduled
    post that uses them goes out. A file on a computer, not at a URL: POST /media/uploads.

    Share links (rolling out: switched on account by account, for some accounts first; until then a
    share link is imported exactly as before): where they are on, a Google Drive, Dropbox, OneDrive or
    SharePoint link of a file shared with "Anyone with the link" is turned into the address of the file
    itself and imported like any URL, under the name the provider gives the file, on the paid plans. A
    file the provider gives no name is saved as file.<ext> (for example file.mp4), and a Dropbox file
    without one under the file name in its link. A link that cannot give one file is refused before
    anything is imported (400 with its own code, next_step and provider), and so is a link that needs
    converting sent with a Free key (403 plan_limit_reached); a link that already downloads the file (a
    drive.usercontent.google.com link, a Google Drive uc link with export=download, a OneDrive or
    SharePoint download.aspx?share= link) is imported on every plan, with a Free key exactly as before.
    A refusal decided from the link or the plan does not start the 20-second wait.

    Args:
        idempotency_key (str | Unset):
        body (MediaImportRequest):  Example: {'url': 'https://example.com/video.mp4'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MediaError | MediaImportReady | MediaImportStarted
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
