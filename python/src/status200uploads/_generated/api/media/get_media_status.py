from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.media_error import MediaError
from ...models.media_status import MediaStatus
from ...types import UNSET, Response


def _get_kwargs(
    *,
    file_id: UUID,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_file_id = str(file_id)
    params["file_id"] = json_file_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/media",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> MediaError | MediaStatus:
    if response.status_code == 200:
        response_200 = MediaStatus.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = MediaError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = MediaError.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = MediaError.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = MediaError.from_dict(response.json())

        return response_500

    response_default = MediaError.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MediaError | MediaStatus]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    file_id: UUID,
) -> Response[MediaError | MediaStatus]:
    """Follow an import

     Status checks are not throttled and not counted.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MediaError | MediaStatus]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    file_id: UUID,
) -> MediaError | MediaStatus | None:
    """Follow an import

     Status checks are not throttled and not counted.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MediaError | MediaStatus
    """

    return sync_detailed(
        client=client,
        file_id=file_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    file_id: UUID,
) -> Response[MediaError | MediaStatus]:
    """Follow an import

     Status checks are not throttled and not counted.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MediaError | MediaStatus]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    file_id: UUID,
) -> MediaError | MediaStatus | None:
    """Follow an import

     Status checks are not throttled and not counted.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MediaError | MediaStatus
    """

    return (
        await asyncio_detailed(
            client=client,
            file_id=file_id,
        )
    ).parsed
