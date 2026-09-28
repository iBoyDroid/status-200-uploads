from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.accepted import Accepted
from ...models.dry_run_report import DryRunReport
from ...models.error_response import ErrorResponse
from ...models.post_request import PostRequest
from ...models.publish_result import PublishResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PostRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/posts",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Accepted | DryRunReport | PublishResult | ErrorResponse:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> DryRunReport | PublishResult:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = DryRunReport.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = PublishResult.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = Accepted.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = ErrorResponse.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Accepted | DryRunReport | PublishResult | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[Accepted | DryRunReport | PublishResult | ErrorResponse]:
    """Publish, schedule or check a post

     One post to one network. Without post.scheduledFor (or with a time within 60 seconds) it is
    published now; more than 60 seconds ahead (up to 365 days) it is scheduled and the answer is 202
    with code "scheduled". With dryRun true every check a publish makes is run and nothing is sent: the
    answer is 200 with dry_run true.

    Order of checks on this address: method, JSON, key, dryRun flag (a dry run is forwarded here), post,
    platform, YouTube tags, scheduledFor, Idempotency-Key, accountId, profile (403 or 400), media ids
    exist (404); then the engine: the X/Skool plan gate (403), the 20-second throttle (429), connection,
    media wait (about 12 seconds here, then 409), pre-post guards, the scheduled branch (202), the
    allowance (429 monthly or 202 queued), the send.

    Media is required except for text posts on X, LinkedIn, Threads, Skool and Facebook. Every answer
    arrives within about 25 seconds; a network slower than that is answered 202 still_publishing. Every
    2xx may carry warnings (fields that were not used) and, when a post or a scheduled post was
    recorded, status200.

    A network's own refusal keeps the network's own 4xx status: pinterest_rejected (Pinterest) and
    x_rejected (X) are listed under every status those networks answer with.

    Args:
        idempotency_key (str | Unset):
        body (PostRequest): A field this API does not read never refuses a post: the answer names
            it in warnings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Accepted | DryRunReport | PublishResult | ErrorResponse]
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
    body: PostRequest,
    idempotency_key: str | Unset = UNSET,
) -> Accepted | DryRunReport | PublishResult | ErrorResponse | None:
    """Publish, schedule or check a post

     One post to one network. Without post.scheduledFor (or with a time within 60 seconds) it is
    published now; more than 60 seconds ahead (up to 365 days) it is scheduled and the answer is 202
    with code "scheduled". With dryRun true every check a publish makes is run and nothing is sent: the
    answer is 200 with dry_run true.

    Order of checks on this address: method, JSON, key, dryRun flag (a dry run is forwarded here), post,
    platform, YouTube tags, scheduledFor, Idempotency-Key, accountId, profile (403 or 400), media ids
    exist (404); then the engine: the X/Skool plan gate (403), the 20-second throttle (429), connection,
    media wait (about 12 seconds here, then 409), pre-post guards, the scheduled branch (202), the
    allowance (429 monthly or 202 queued), the send.

    Media is required except for text posts on X, LinkedIn, Threads, Skool and Facebook. Every answer
    arrives within about 25 seconds; a network slower than that is answered 202 still_publishing. Every
    2xx may carry warnings (fields that were not used) and, when a post or a scheduled post was
    recorded, status200.

    A network's own refusal keeps the network's own 4xx status: pinterest_rejected (Pinterest) and
    x_rejected (X) are listed under every status those networks answer with.

    Args:
        idempotency_key (str | Unset):
        body (PostRequest): A field this API does not read never refuses a post: the answer names
            it in warnings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Accepted | DryRunReport | PublishResult | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[Accepted | DryRunReport | PublishResult | ErrorResponse]:
    """Publish, schedule or check a post

     One post to one network. Without post.scheduledFor (or with a time within 60 seconds) it is
    published now; more than 60 seconds ahead (up to 365 days) it is scheduled and the answer is 202
    with code "scheduled". With dryRun true every check a publish makes is run and nothing is sent: the
    answer is 200 with dry_run true.

    Order of checks on this address: method, JSON, key, dryRun flag (a dry run is forwarded here), post,
    platform, YouTube tags, scheduledFor, Idempotency-Key, accountId, profile (403 or 400), media ids
    exist (404); then the engine: the X/Skool plan gate (403), the 20-second throttle (429), connection,
    media wait (about 12 seconds here, then 409), pre-post guards, the scheduled branch (202), the
    allowance (429 monthly or 202 queued), the send.

    Media is required except for text posts on X, LinkedIn, Threads, Skool and Facebook. Every answer
    arrives within about 25 seconds; a network slower than that is answered 202 still_publishing. Every
    2xx may carry warnings (fields that were not used) and, when a post or a scheduled post was
    recorded, status200.

    A network's own refusal keeps the network's own 4xx status: pinterest_rejected (Pinterest) and
    x_rejected (X) are listed under every status those networks answer with.

    Args:
        idempotency_key (str | Unset):
        body (PostRequest): A field this API does not read never refuses a post: the answer names
            it in warnings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Accepted | DryRunReport | PublishResult | ErrorResponse]
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
    body: PostRequest,
    idempotency_key: str | Unset = UNSET,
) -> Accepted | DryRunReport | PublishResult | ErrorResponse | None:
    """Publish, schedule or check a post

     One post to one network. Without post.scheduledFor (or with a time within 60 seconds) it is
    published now; more than 60 seconds ahead (up to 365 days) it is scheduled and the answer is 202
    with code "scheduled". With dryRun true every check a publish makes is run and nothing is sent: the
    answer is 200 with dry_run true.

    Order of checks on this address: method, JSON, key, dryRun flag (a dry run is forwarded here), post,
    platform, YouTube tags, scheduledFor, Idempotency-Key, accountId, profile (403 or 400), media ids
    exist (404); then the engine: the X/Skool plan gate (403), the 20-second throttle (429), connection,
    media wait (about 12 seconds here, then 409), pre-post guards, the scheduled branch (202), the
    allowance (429 monthly or 202 queued), the send.

    Media is required except for text posts on X, LinkedIn, Threads, Skool and Facebook. Every answer
    arrives within about 25 seconds; a network slower than that is answered 202 still_publishing. Every
    2xx may carry warnings (fields that were not used) and, when a post or a scheduled post was
    recorded, status200.

    A network's own refusal keeps the network's own 4xx status: pinterest_rejected (Pinterest) and
    x_rejected (X) are listed under every status those networks answer with.

    Args:
        idempotency_key (str | Unset):
        body (PostRequest): A field this API does not read never refuses a post: the answer names
            it in warnings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Accepted | DryRunReport | PublishResult | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
