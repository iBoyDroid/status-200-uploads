from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.upload_link_error_response import UploadLinkErrorResponse
from ...models.upload_ready import UploadReady
from ...models.upload_verifying import UploadVerifying
from ...types import Response


def _get_kwargs(
    file_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/media/uploads/{file_id}/complete".format(
            file_id=quote(str(file_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> UploadLinkErrorResponse | UploadReady | UploadVerifying:
    if response.status_code == 200:
        response_200 = UploadReady.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = UploadVerifying.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = UploadLinkErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UploadLinkErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = UploadLinkErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UploadLinkErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = UploadLinkErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 410:
        response_410 = UploadLinkErrorResponse.from_dict(response.json())

        return response_410

    if response.status_code == 422:
        response_422 = UploadLinkErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = UploadLinkErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = UploadLinkErrorResponse.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = UploadLinkErrorResponse.from_dict(response.json())

        return response_503

    response_default = UploadLinkErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[UploadLinkErrorResponse | UploadReady | UploadVerifying]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[UploadLinkErrorResponse | UploadReady | UploadVerifying]:
    """Check an uploaded file and put it in the media library

     Call it once the whole file was sent (the uploader exited 0). The file that arrived is checked: its
    exact size, its type and first bytes, and its SHA-256. 200 ready: it is in the media library;
    publish it with this file_id in post.content.mediaID. 202 verifying: the check is still running (a 5
    GB file can take about 15 minutes); poll GET /media?file_id= every 15 seconds until it says ready,
    and never upload the file again: it finishes on its own. A check delayed by a temporary problem on
    our side answers 202 with a longer Retry-After and retries by itself. No body. Any API key of the
    account may call it, and calling it again is harmless (a ready upload answers 200 again).

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadLinkErrorResponse | UploadReady | UploadVerifying]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> UploadLinkErrorResponse | UploadReady | UploadVerifying | None:
    """Check an uploaded file and put it in the media library

     Call it once the whole file was sent (the uploader exited 0). The file that arrived is checked: its
    exact size, its type and first bytes, and its SHA-256. 200 ready: it is in the media library;
    publish it with this file_id in post.content.mediaID. 202 verifying: the check is still running (a 5
    GB file can take about 15 minutes); poll GET /media?file_id= every 15 seconds until it says ready,
    and never upload the file again: it finishes on its own. A check delayed by a temporary problem on
    our side answers 202 with a longer Retry-After and retries by itself. No body. Any API key of the
    account may call it, and calling it again is harmless (a ready upload answers 200 again).

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadLinkErrorResponse | UploadReady | UploadVerifying
    """

    return sync_detailed(
        file_id=file_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[UploadLinkErrorResponse | UploadReady | UploadVerifying]:
    """Check an uploaded file and put it in the media library

     Call it once the whole file was sent (the uploader exited 0). The file that arrived is checked: its
    exact size, its type and first bytes, and its SHA-256. 200 ready: it is in the media library;
    publish it with this file_id in post.content.mediaID. 202 verifying: the check is still running (a 5
    GB file can take about 15 minutes); poll GET /media?file_id= every 15 seconds until it says ready,
    and never upload the file again: it finishes on its own. A check delayed by a temporary problem on
    our side answers 202 with a longer Retry-After and retries by itself. No body. Any API key of the
    account may call it, and calling it again is harmless (a ready upload answers 200 again).

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadLinkErrorResponse | UploadReady | UploadVerifying]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> UploadLinkErrorResponse | UploadReady | UploadVerifying | None:
    """Check an uploaded file and put it in the media library

     Call it once the whole file was sent (the uploader exited 0). The file that arrived is checked: its
    exact size, its type and first bytes, and its SHA-256. 200 ready: it is in the media library;
    publish it with this file_id in post.content.mediaID. 202 verifying: the check is still running (a 5
    GB file can take about 15 minutes); poll GET /media?file_id= every 15 seconds until it says ready,
    and never upload the file again: it finishes on its own. A check delayed by a temporary problem on
    our side answers 202 with a longer Retry-After and retries by itself. No body. Any API key of the
    account may call it, and calling it again is harmless (a ready upload answers 200 again).

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadLinkErrorResponse | UploadReady | UploadVerifying
    """

    return (
        await asyncio_detailed(
            file_id=file_id,
            client=client,
        )
    ).parsed
