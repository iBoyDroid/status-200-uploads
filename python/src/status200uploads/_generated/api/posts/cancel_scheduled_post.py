from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.cancel_result import CancelResult
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/posts/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CancelResult | ErrorResponse:
    if response.status_code == 200:
        response_200 = CancelResult.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if response.status_code == 504:
        response_504 = ErrorResponse.from_dict(response.json())

        return response_504

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CancelResult | ErrorResponse]:
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
) -> Response[CancelResult | ErrorResponse]:
    """Cancel a post that has not gone out

     The id is a scheduled_post_id (from a 202 scheduled or queued answer, or any waiting post of yours:
    API, dashboard, AI connector or the next-day queue). No body. Cancelling twice is safe: the second
    answer is 200 with already_cancelled true. The key is checked first (401), then the id (400), then
    the engine cancels it. The Idempotency-Key header is ignored.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelResult | ErrorResponse]
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
) -> CancelResult | ErrorResponse | None:
    """Cancel a post that has not gone out

     The id is a scheduled_post_id (from a 202 scheduled or queued answer, or any waiting post of yours:
    API, dashboard, AI connector or the next-day queue). No body. Cancelling twice is safe: the second
    answer is 200 with already_cancelled true. The key is checked first (401), then the id (400), then
    the engine cancels it. The Idempotency-Key header is ignored.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelResult | ErrorResponse
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CancelResult | ErrorResponse]:
    """Cancel a post that has not gone out

     The id is a scheduled_post_id (from a 202 scheduled or queued answer, or any waiting post of yours:
    API, dashboard, AI connector or the next-day queue). No body. Cancelling twice is safe: the second
    answer is 200 with already_cancelled true. The key is checked first (401), then the id (400), then
    the engine cancels it. The Idempotency-Key header is ignored.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelResult | ErrorResponse]
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
) -> CancelResult | ErrorResponse | None:
    """Cancel a post that has not gone out

     The id is a scheduled_post_id (from a 202 scheduled or queued answer, or any waiting post of yours:
    API, dashboard, AI connector or the next-day queue). No body. Cancelling twice is safe: the second
    answer is 200 with already_cancelled true. The key is checked first (401), then the id (400), then
    the engine cancels it. The Idempotency-Key header is ignored.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelResult | ErrorResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
