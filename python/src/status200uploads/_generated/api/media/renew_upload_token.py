from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.upload_link import UploadLink
from ...models.upload_link_error_response import UploadLinkErrorResponse
from ...models.upload_token_request import UploadTokenRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    file_id: UUID,
    *,
    body: UploadTokenRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/media/uploads/{file_id}/token".format(
            file_id=quote(str(file_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> UploadLink | UploadLinkErrorResponse:
    if response.status_code == 200:
        response_200 = UploadLink.from_dict(response.json())

        return response_200

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
) -> Response[UploadLink | UploadLinkErrorResponse]:
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
    body: UploadTokenRequest | Unset = UNSET,
) -> Response[UploadLink | UploadLinkErrorResponse]:
    """A fresh token for an unfinished upload

     When the token expired before the whole file was sent (the uploader's exit 4, or storage answering
    400 about the token): the same upload.url with a new upload.token, and with shell a new
    uploader.command, so the upload continues where it stopped. Only the API key that made the link can
    renew it (another key of the account gets 404), at most 12 times and within 24 hours of the link,
    and only while the whole file has not arrived (then 409 upload_already_received: complete it). A
    closed upload answers what completing it would (409, 410 or 422). The body is optional: shell,
    runner and max_run_seconds as for a new link; without them the answer has no uploader block.

    Args:
        file_id (UUID):
        body (UploadTokenRequest | Unset): Optional. The file's name, size and SHA-256 are the
            link's own and are not sent again.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadLink | UploadLinkErrorResponse]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadTokenRequest | Unset = UNSET,
) -> UploadLink | UploadLinkErrorResponse | None:
    """A fresh token for an unfinished upload

     When the token expired before the whole file was sent (the uploader's exit 4, or storage answering
    400 about the token): the same upload.url with a new upload.token, and with shell a new
    uploader.command, so the upload continues where it stopped. Only the API key that made the link can
    renew it (another key of the account gets 404), at most 12 times and within 24 hours of the link,
    and only while the whole file has not arrived (then 409 upload_already_received: complete it). A
    closed upload answers what completing it would (409, 410 or 422). The body is optional: shell,
    runner and max_run_seconds as for a new link; without them the answer has no uploader block.

    Args:
        file_id (UUID):
        body (UploadTokenRequest | Unset): Optional. The file's name, size and SHA-256 are the
            link's own and are not sent again.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadLink | UploadLinkErrorResponse
    """

    return sync_detailed(
        file_id=file_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadTokenRequest | Unset = UNSET,
) -> Response[UploadLink | UploadLinkErrorResponse]:
    """A fresh token for an unfinished upload

     When the token expired before the whole file was sent (the uploader's exit 4, or storage answering
    400 about the token): the same upload.url with a new upload.token, and with shell a new
    uploader.command, so the upload continues where it stopped. Only the API key that made the link can
    renew it (another key of the account gets 404), at most 12 times and within 24 hours of the link,
    and only while the whole file has not arrived (then 409 upload_already_received: complete it). A
    closed upload answers what completing it would (409, 410 or 422). The body is optional: shell,
    runner and max_run_seconds as for a new link; without them the answer has no uploader block.

    Args:
        file_id (UUID):
        body (UploadTokenRequest | Unset): Optional. The file's name, size and SHA-256 are the
            link's own and are not sent again.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadLink | UploadLinkErrorResponse]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadTokenRequest | Unset = UNSET,
) -> UploadLink | UploadLinkErrorResponse | None:
    """A fresh token for an unfinished upload

     When the token expired before the whole file was sent (the uploader's exit 4, or storage answering
    400 about the token): the same upload.url with a new upload.token, and with shell a new
    uploader.command, so the upload continues where it stopped. Only the API key that made the link can
    renew it (another key of the account gets 404), at most 12 times and within 24 hours of the link,
    and only while the whole file has not arrived (then 409 upload_already_received: complete it). A
    closed upload answers what completing it would (409, 410 or 422). The body is optional: shell,
    runner and max_run_seconds as for a new link; without them the answer has no uploader block.

    Args:
        file_id (UUID):
        body (UploadTokenRequest | Unset): Optional. The file's name, size and SHA-256 are the
            link's own and are not sent again.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadLink | UploadLinkErrorResponse
    """

    return (
        await asyncio_detailed(
            file_id=file_id,
            client=client,
            body=body,
        )
    ).parsed
