from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_posts_kind import ListPostsKind
from ...models.list_posts_status_item import ListPostsStatusItem
from ...models.platform import Platform
from ...models.post_list import PostList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    status: list[ListPostsStatusItem] | Unset = UNSET,
    platform: Platform | Unset = UNSET,
    kind: ListPostsKind | Unset = UNSET,
    profile_id: UUID | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_status: list[str] | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item: str = status_item_data
            json_status.append(status_item)

    params["status"] = json_status

    json_platform: str | Unset = UNSET
    if not isinstance(platform, Unset):
        json_platform = platform

    params["platform"] = json_platform

    json_kind: str | Unset = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind

    params["kind"] = json_kind

    json_profile_id: str | Unset = UNSET
    if not isinstance(profile_id, Unset):
        json_profile_id = str(profile_id)
    params["profile_id"] = json_profile_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/posts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | PostList:
    if response.status_code == 200:
        response_200 = PostList.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

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
) -> Response[ErrorResponse | PostList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    status: list[ListPostsStatusItem] | Unset = UNSET,
    platform: Platform | Unset = UNSET,
    kind: ListPostsKind | Unset = UNSET,
    profile_id: UUID | Unset = UNSET,
) -> Response[ErrorResponse | PostList]:
    """List your posts and waiting posts

     Newest first by `at` (when a post was sent, when a scheduled post is due). A scheduled post is
    listed until it has produced posts; then each network's post is listed instead, with its
    scheduled_post_id. 60 reads a minute per account (all its keys together). Not counted in the key's
    request count, and a 200 is not logged.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        status (list[ListPostsStatusItem] | Unset):
        platform (Platform | Unset):
        kind (ListPostsKind | Unset):
        profile_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PostList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
        platform=platform,
        kind=kind,
        profile_id=profile_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    status: list[ListPostsStatusItem] | Unset = UNSET,
    platform: Platform | Unset = UNSET,
    kind: ListPostsKind | Unset = UNSET,
    profile_id: UUID | Unset = UNSET,
) -> ErrorResponse | PostList | None:
    """List your posts and waiting posts

     Newest first by `at` (when a post was sent, when a scheduled post is due). A scheduled post is
    listed until it has produced posts; then each network's post is listed instead, with its
    scheduled_post_id. 60 reads a minute per account (all its keys together). Not counted in the key's
    request count, and a 200 is not logged.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        status (list[ListPostsStatusItem] | Unset):
        platform (Platform | Unset):
        kind (ListPostsKind | Unset):
        profile_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PostList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        status=status,
        platform=platform,
        kind=kind,
        profile_id=profile_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    status: list[ListPostsStatusItem] | Unset = UNSET,
    platform: Platform | Unset = UNSET,
    kind: ListPostsKind | Unset = UNSET,
    profile_id: UUID | Unset = UNSET,
) -> Response[ErrorResponse | PostList]:
    """List your posts and waiting posts

     Newest first by `at` (when a post was sent, when a scheduled post is due). A scheduled post is
    listed until it has produced posts; then each network's post is listed instead, with its
    scheduled_post_id. 60 reads a minute per account (all its keys together). Not counted in the key's
    request count, and a 200 is not logged.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        status (list[ListPostsStatusItem] | Unset):
        platform (Platform | Unset):
        kind (ListPostsKind | Unset):
        profile_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PostList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
        platform=platform,
        kind=kind,
        profile_id=profile_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    status: list[ListPostsStatusItem] | Unset = UNSET,
    platform: Platform | Unset = UNSET,
    kind: ListPostsKind | Unset = UNSET,
    profile_id: UUID | Unset = UNSET,
) -> ErrorResponse | PostList | None:
    """List your posts and waiting posts

     Newest first by `at` (when a post was sent, when a scheduled post is due). A scheduled post is
    listed until it has produced posts; then each network's post is listed instead, with its
    scheduled_post_id. 60 reads a minute per account (all its keys together). Not counted in the key's
    request count, and a 200 is not logged.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        status (list[ListPostsStatusItem] | Unset):
        platform (Platform | Unset):
        kind (ListPostsKind | Unset):
        profile_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PostList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            status=status,
            platform=platform,
            kind=kind,
            profile_id=profile_id,
        )
    ).parsed
