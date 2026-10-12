from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.upload_cancelled import UploadCancelled
from ...models.upload_link_error_response import UploadLinkErrorResponse
from ...types import Response


def _get_kwargs(
    file_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/media/uploads/{file_id}".format(
            file_id=quote(str(file_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> UploadCancelled | UploadLinkErrorResponse:
    if response.status_code == 200:
        response_200 = UploadCancelled.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = UploadLinkErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = UploadLinkErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = UploadLinkErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = UploadLinkErrorResponse.from_dict(response.json())

        return response_409

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
) -> Response[UploadCancelled | UploadLinkErrorResponse]:
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
) -> Response[UploadCancelled | UploadLinkErrorResponse]:
    """Cancel an unfinished upload

     Closes an upload that is not ready: what arrived is deleted within a few minutes, and its slot among
    the 10 open uploads frees at once. Bytes that already arrived still count in today's budget. It
    works while making links is paused. A ready upload is a media library file: delete it there (409
    upload_closed). Any API key of the account; no body.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadCancelled | UploadLinkErrorResponse]
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
) -> UploadCancelled | UploadLinkErrorResponse | None:
    """Cancel an unfinished upload

     Closes an upload that is not ready: what arrived is deleted within a few minutes, and its slot among
    the 10 open uploads frees at once. Bytes that already arrived still count in today's budget. It
    works while making links is paused. A ready upload is a media library file: delete it there (409
    upload_closed). Any API key of the account; no body.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadCancelled | UploadLinkErrorResponse
    """

    return sync_detailed(
        file_id=file_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[UploadCancelled | UploadLinkErrorResponse]:
    """Cancel an unfinished upload

     Closes an upload that is not ready: what arrived is deleted within a few minutes, and its slot among
    the 10 open uploads frees at once. Bytes that already arrived still count in today's budget. It
    works while making links is paused. A ready upload is a media library file: delete it there (409
    upload_closed). Any API key of the account; no body.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadCancelled | UploadLinkErrorResponse]
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
) -> UploadCancelled | UploadLinkErrorResponse | None:
    """Cancel an unfinished upload

     Closes an upload that is not ready: what arrived is deleted within a few minutes, and its slot among
    the 10 open uploads frees at once. Bytes that already arrived still count in today's budget. It
    works while making links is paused. A ready upload is a media library file: delete it there (409
    upload_closed). Any API key of the account; no body.

    Args:
        file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadCancelled | UploadLinkErrorResponse
    """

    return (
        await asyncio_detailed(
            file_id=file_id,
            client=client,
        )
    ).parsed
