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

     Images up to 20 MB, videos up to 5 GB. The source is probed first (a HEAD, then a 1-byte ranged GET,
    8 seconds each, so up to about 16 seconds). The request waits up to about 22 seconds for the import:
    200 ready, otherwise 202 processing (at once when the declared size cannot finish in time). One
    import every 20 seconds per account. Files are kept for 7 days, and until a scheduled post that uses
    them goes out.

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

     Images up to 20 MB, videos up to 5 GB. The source is probed first (a HEAD, then a 1-byte ranged GET,
    8 seconds each, so up to about 16 seconds). The request waits up to about 22 seconds for the import:
    200 ready, otherwise 202 processing (at once when the declared size cannot finish in time). One
    import every 20 seconds per account. Files are kept for 7 days, and until a scheduled post that uses
    them goes out.

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

     Images up to 20 MB, videos up to 5 GB. The source is probed first (a HEAD, then a 1-byte ranged GET,
    8 seconds each, so up to about 16 seconds). The request waits up to about 22 seconds for the import:
    200 ready, otherwise 202 processing (at once when the declared size cannot finish in time). One
    import every 20 seconds per account. Files are kept for 7 days, and until a scheduled post that uses
    them goes out.

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

     Images up to 20 MB, videos up to 5 GB. The source is probed first (a HEAD, then a 1-byte ranged GET,
    8 seconds each, so up to about 16 seconds). The request waits up to about 22 seconds for the import:
    200 ready, otherwise 202 processing (at once when the declared size cannot finish in time). One
    import every 20 seconds per account. Files are kept for 7 days, and until a scheduled post that uses
    them goes out.

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
