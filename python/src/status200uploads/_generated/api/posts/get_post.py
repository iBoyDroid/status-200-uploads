from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.post_read import PostRead
from ...types import Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/posts/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | PostRead:
    if response.status_code == 200:
        response_200 = PostRead.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | PostRead]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | PostRead]:
    """Read one post or scheduled post

     The id is status200.post_id or status200.scheduled_post_id of a POST answer (its
    status200.status_url is this address), or an id from GET /posts. To wait for a post, read it every
    30 seconds until done is true, for up to 10 minutes. Another account's id is answered exactly like
    an id that does not exist.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PostRead]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | PostRead | None:
    """Read one post or scheduled post

     The id is status200.post_id or status200.scheduled_post_id of a POST answer (its
    status200.status_url is this address), or an id from GET /posts. To wait for a post, read it every
    30 seconds until done is true, for up to 10 minutes. Another account's id is answered exactly like
    an id that does not exist.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PostRead
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | PostRead]:
    """Read one post or scheduled post

     The id is status200.post_id or status200.scheduled_post_id of a POST answer (its
    status200.status_url is this address), or an id from GET /posts. To wait for a post, read it every
    30 seconds until done is true, for up to 10 minutes. Another account's id is answered exactly like
    an id that does not exist.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PostRead]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | PostRead | None:
    """Read one post or scheduled post

     The id is status200.post_id or status200.scheduled_post_id of a POST answer (its
    status200.status_url is this address), or an id from GET /posts. To wait for a post, read it every
    30 seconds until done is true, for up to 10 minutes. Another account's id is answered exactly like
    an id that does not exist.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PostRead
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
