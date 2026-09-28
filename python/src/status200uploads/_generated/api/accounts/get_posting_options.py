from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.platform import Platform
from ...models.posting_options import PostingOptions
from ...types import UNSET, Response, Unset


def _get_kwargs(
    profile_id: UUID,
    *,
    platforms: list[Platform] | Unset = UNSET,
    skool_group_slug: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_platforms: list[str] | Unset = UNSET
    if not isinstance(platforms, Unset):
        json_platforms = []
        for platforms_item_data in platforms:
            platforms_item: str = platforms_item_data
            json_platforms.append(platforms_item)

    params["platforms"] = json_platforms

    params["skool_group_slug"] = skool_group_slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{profile_id}/options".format(
            profile_id=quote(str(profile_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | PostingOptions:
    if response.status_code == 200:
        response_200 = PostingOptions.from_dict(response.json())

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
) -> Response[ErrorResponse | PostingOptions]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    profile_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    platforms: list[Platform] | Unset = UNSET,
    skool_group_slug: str | Unset = UNSET,
) -> Response[ErrorResponse | PostingOptions]:
    """What a profile may do on each network

     Asked of the networks themselves with the profile's own sign-in: the TikTok privacy levels it
    accepts, Pinterest boards, Skool groups and labels, the Facebook Page, the Instagram publishing
    limit, YouTube's choices. One row per network, always 200 (a network that fails is a row). Answers
    are reused for 90 seconds, and the whole answer is ready within 20 seconds. Also 10 a minute per
    account, on top of the 60 reads.

    Args:
        profile_id (UUID):
        platforms (list[Platform] | Unset):
        skool_group_slug (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PostingOptions]
    """

    kwargs = _get_kwargs(
        profile_id=profile_id,
        platforms=platforms,
        skool_group_slug=skool_group_slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    profile_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    platforms: list[Platform] | Unset = UNSET,
    skool_group_slug: str | Unset = UNSET,
) -> ErrorResponse | PostingOptions | None:
    """What a profile may do on each network

     Asked of the networks themselves with the profile's own sign-in: the TikTok privacy levels it
    accepts, Pinterest boards, Skool groups and labels, the Facebook Page, the Instagram publishing
    limit, YouTube's choices. One row per network, always 200 (a network that fails is a row). Answers
    are reused for 90 seconds, and the whole answer is ready within 20 seconds. Also 10 a minute per
    account, on top of the 60 reads.

    Args:
        profile_id (UUID):
        platforms (list[Platform] | Unset):
        skool_group_slug (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PostingOptions
    """

    return sync_detailed(
        profile_id=profile_id,
        client=client,
        platforms=platforms,
        skool_group_slug=skool_group_slug,
    ).parsed


async def asyncio_detailed(
    profile_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    platforms: list[Platform] | Unset = UNSET,
    skool_group_slug: str | Unset = UNSET,
) -> Response[ErrorResponse | PostingOptions]:
    """What a profile may do on each network

     Asked of the networks themselves with the profile's own sign-in: the TikTok privacy levels it
    accepts, Pinterest boards, Skool groups and labels, the Facebook Page, the Instagram publishing
    limit, YouTube's choices. One row per network, always 200 (a network that fails is a row). Answers
    are reused for 90 seconds, and the whole answer is ready within 20 seconds. Also 10 a minute per
    account, on top of the 60 reads.

    Args:
        profile_id (UUID):
        platforms (list[Platform] | Unset):
        skool_group_slug (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PostingOptions]
    """

    kwargs = _get_kwargs(
        profile_id=profile_id,
        platforms=platforms,
        skool_group_slug=skool_group_slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    profile_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    platforms: list[Platform] | Unset = UNSET,
    skool_group_slug: str | Unset = UNSET,
) -> ErrorResponse | PostingOptions | None:
    """What a profile may do on each network

     Asked of the networks themselves with the profile's own sign-in: the TikTok privacy levels it
    accepts, Pinterest boards, Skool groups and labels, the Facebook Page, the Instagram publishing
    limit, YouTube's choices. One row per network, always 200 (a network that fails is a row). Answers
    are reused for 90 seconds, and the whole answer is ready within 20 seconds. Also 10 a minute per
    account, on top of the 60 reads.

    Args:
        profile_id (UUID):
        platforms (list[Platform] | Unset):
        skool_group_slug (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PostingOptions
    """

    return (
        await asyncio_detailed(
            profile_id=profile_id,
            client=client,
            platforms=platforms,
            skool_group_slug=skool_group_slug,
        )
    ).parsed
