from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.upload_link import UploadLink
from ...models.upload_link_error_response import UploadLinkErrorResponse
from ...models.upload_link_request import UploadLinkRequest
from ...types import Response


def _get_kwargs(
    *,
    body: UploadLinkRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/media/uploads",
    }

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

    if response.status_code == 201:
        response_201 = UploadLink.from_dict(response.json())

        return response_201

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

    if response.status_code == 413:
        response_413 = UploadLinkErrorResponse.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = UploadLinkErrorResponse.from_dict(response.json())

        return response_415

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
    *,
    client: AuthenticatedClient | Client,
    body: UploadLinkRequest,
) -> Response[UploadLink | UploadLinkErrorResponse]:
    """Make a one-time upload link for a file on a computer

     For a script, or an AI app that runs commands (tested with Claude Code; other AI apps that can run
    commands may work), that has the file on its own computer. Send the file's name, its exact size in
    bytes and its SHA-256. The answer is a one-time TUS 1.0.0 address on storage's own host (upload.url)
    with a signed token (upload.token), and, when shell is sent, a ready-made command (uploader.command)
    that downloads our uploader, checks its SHA-256 and sends the file. Once the whole file is sent,
    POST /media/uploads/{file_id}/complete has it checked (exact size, type, first bytes and SHA-256)
    and put in the media library; the file_id then goes in post.content.mediaID like an imported file's.
    Nothing is public before that check.

    With your own TUS client: HEAD upload.url for its Upload-Offset, then PATCH pieces of exactly
    chunk_size bytes (6 MiB; the last one shorter) from that offset, each with x-signature
    (upload.token), Tus-Resumable 1.0.0, Upload-Offset and Content-Type application/offset+octet-stream;
    after a failed PATCH, HEAD again and go on from the offset it gives. The token works for this one
    file only, for about 2 hours (a fresh one: POST /media/uploads/{file_id}/token). A stopped upload
    can be continued until upload.resume_before; after that, what was sent is deleted. The same file
    (sha256 and size) asked for again from the same API key while its link is open gets the same address
    with a fresh token: 200 with renewed true, and nothing is reserved twice.

    Paid plans only: Free and an unknown plan are refused with 403 plan_limit_reached before anything is
    reserved (upload the file in the dashboard, Media, which every plan can use). One daily budget per
    account and UTC day counts every upload link (from any key or app) and the URL imports of connected
    AI apps: Beginner 2 GB, Apprentice 10 GB, Skilled 25 GB, Expert and Agency 100 GB; uploading in the
    dashboard has no daily budget. A link holds its size until it closes, and bytes that arrived still
    count when the check refuses them or the upload is cancelled. Per account: 10 uploads open at once,
    20 new links in 10 minutes and 100 a day, and 60 upload-link calls a minute (new links, tokens,
    complete and cancel together).

    These answers also carry next_step (what to do next, in a sentence) and most refusals retry
    ("never", or "after_reset" for a budget that frees at 00:00 UTC), because the AI connector reads the
    same answers; the schemas and the examples leave both out. The request log keeps a summary of each
    answer (ids, status, type, size and times), never the token, the upload address or the command.

    Args:
        body (UploadLinkRequest): file_id is not part of a new link (400): a fresh token for an
            unfinished upload is POST /media/uploads/{file_id}/token. Other fields are not read.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadLink | UploadLinkErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: UploadLinkRequest,
) -> UploadLink | UploadLinkErrorResponse | None:
    """Make a one-time upload link for a file on a computer

     For a script, or an AI app that runs commands (tested with Claude Code; other AI apps that can run
    commands may work), that has the file on its own computer. Send the file's name, its exact size in
    bytes and its SHA-256. The answer is a one-time TUS 1.0.0 address on storage's own host (upload.url)
    with a signed token (upload.token), and, when shell is sent, a ready-made command (uploader.command)
    that downloads our uploader, checks its SHA-256 and sends the file. Once the whole file is sent,
    POST /media/uploads/{file_id}/complete has it checked (exact size, type, first bytes and SHA-256)
    and put in the media library; the file_id then goes in post.content.mediaID like an imported file's.
    Nothing is public before that check.

    With your own TUS client: HEAD upload.url for its Upload-Offset, then PATCH pieces of exactly
    chunk_size bytes (6 MiB; the last one shorter) from that offset, each with x-signature
    (upload.token), Tus-Resumable 1.0.0, Upload-Offset and Content-Type application/offset+octet-stream;
    after a failed PATCH, HEAD again and go on from the offset it gives. The token works for this one
    file only, for about 2 hours (a fresh one: POST /media/uploads/{file_id}/token). A stopped upload
    can be continued until upload.resume_before; after that, what was sent is deleted. The same file
    (sha256 and size) asked for again from the same API key while its link is open gets the same address
    with a fresh token: 200 with renewed true, and nothing is reserved twice.

    Paid plans only: Free and an unknown plan are refused with 403 plan_limit_reached before anything is
    reserved (upload the file in the dashboard, Media, which every plan can use). One daily budget per
    account and UTC day counts every upload link (from any key or app) and the URL imports of connected
    AI apps: Beginner 2 GB, Apprentice 10 GB, Skilled 25 GB, Expert and Agency 100 GB; uploading in the
    dashboard has no daily budget. A link holds its size until it closes, and bytes that arrived still
    count when the check refuses them or the upload is cancelled. Per account: 10 uploads open at once,
    20 new links in 10 minutes and 100 a day, and 60 upload-link calls a minute (new links, tokens,
    complete and cancel together).

    These answers also carry next_step (what to do next, in a sentence) and most refusals retry
    ("never", or "after_reset" for a budget that frees at 00:00 UTC), because the AI connector reads the
    same answers; the schemas and the examples leave both out. The request log keeps a summary of each
    answer (ids, status, type, size and times), never the token, the upload address or the command.

    Args:
        body (UploadLinkRequest): file_id is not part of a new link (400): a fresh token for an
            unfinished upload is POST /media/uploads/{file_id}/token. Other fields are not read.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadLink | UploadLinkErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: UploadLinkRequest,
) -> Response[UploadLink | UploadLinkErrorResponse]:
    """Make a one-time upload link for a file on a computer

     For a script, or an AI app that runs commands (tested with Claude Code; other AI apps that can run
    commands may work), that has the file on its own computer. Send the file's name, its exact size in
    bytes and its SHA-256. The answer is a one-time TUS 1.0.0 address on storage's own host (upload.url)
    with a signed token (upload.token), and, when shell is sent, a ready-made command (uploader.command)
    that downloads our uploader, checks its SHA-256 and sends the file. Once the whole file is sent,
    POST /media/uploads/{file_id}/complete has it checked (exact size, type, first bytes and SHA-256)
    and put in the media library; the file_id then goes in post.content.mediaID like an imported file's.
    Nothing is public before that check.

    With your own TUS client: HEAD upload.url for its Upload-Offset, then PATCH pieces of exactly
    chunk_size bytes (6 MiB; the last one shorter) from that offset, each with x-signature
    (upload.token), Tus-Resumable 1.0.0, Upload-Offset and Content-Type application/offset+octet-stream;
    after a failed PATCH, HEAD again and go on from the offset it gives. The token works for this one
    file only, for about 2 hours (a fresh one: POST /media/uploads/{file_id}/token). A stopped upload
    can be continued until upload.resume_before; after that, what was sent is deleted. The same file
    (sha256 and size) asked for again from the same API key while its link is open gets the same address
    with a fresh token: 200 with renewed true, and nothing is reserved twice.

    Paid plans only: Free and an unknown plan are refused with 403 plan_limit_reached before anything is
    reserved (upload the file in the dashboard, Media, which every plan can use). One daily budget per
    account and UTC day counts every upload link (from any key or app) and the URL imports of connected
    AI apps: Beginner 2 GB, Apprentice 10 GB, Skilled 25 GB, Expert and Agency 100 GB; uploading in the
    dashboard has no daily budget. A link holds its size until it closes, and bytes that arrived still
    count when the check refuses them or the upload is cancelled. Per account: 10 uploads open at once,
    20 new links in 10 minutes and 100 a day, and 60 upload-link calls a minute (new links, tokens,
    complete and cancel together).

    These answers also carry next_step (what to do next, in a sentence) and most refusals retry
    ("never", or "after_reset" for a budget that frees at 00:00 UTC), because the AI connector reads the
    same answers; the schemas and the examples leave both out. The request log keeps a summary of each
    answer (ids, status, type, size and times), never the token, the upload address or the command.

    Args:
        body (UploadLinkRequest): file_id is not part of a new link (400): a fresh token for an
            unfinished upload is POST /media/uploads/{file_id}/token. Other fields are not read.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadLink | UploadLinkErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: UploadLinkRequest,
) -> UploadLink | UploadLinkErrorResponse | None:
    """Make a one-time upload link for a file on a computer

     For a script, or an AI app that runs commands (tested with Claude Code; other AI apps that can run
    commands may work), that has the file on its own computer. Send the file's name, its exact size in
    bytes and its SHA-256. The answer is a one-time TUS 1.0.0 address on storage's own host (upload.url)
    with a signed token (upload.token), and, when shell is sent, a ready-made command (uploader.command)
    that downloads our uploader, checks its SHA-256 and sends the file. Once the whole file is sent,
    POST /media/uploads/{file_id}/complete has it checked (exact size, type, first bytes and SHA-256)
    and put in the media library; the file_id then goes in post.content.mediaID like an imported file's.
    Nothing is public before that check.

    With your own TUS client: HEAD upload.url for its Upload-Offset, then PATCH pieces of exactly
    chunk_size bytes (6 MiB; the last one shorter) from that offset, each with x-signature
    (upload.token), Tus-Resumable 1.0.0, Upload-Offset and Content-Type application/offset+octet-stream;
    after a failed PATCH, HEAD again and go on from the offset it gives. The token works for this one
    file only, for about 2 hours (a fresh one: POST /media/uploads/{file_id}/token). A stopped upload
    can be continued until upload.resume_before; after that, what was sent is deleted. The same file
    (sha256 and size) asked for again from the same API key while its link is open gets the same address
    with a fresh token: 200 with renewed true, and nothing is reserved twice.

    Paid plans only: Free and an unknown plan are refused with 403 plan_limit_reached before anything is
    reserved (upload the file in the dashboard, Media, which every plan can use). One daily budget per
    account and UTC day counts every upload link (from any key or app) and the URL imports of connected
    AI apps: Beginner 2 GB, Apprentice 10 GB, Skilled 25 GB, Expert and Agency 100 GB; uploading in the
    dashboard has no daily budget. A link holds its size until it closes, and bytes that arrived still
    count when the check refuses them or the upload is cancelled. Per account: 10 uploads open at once,
    20 new links in 10 minutes and 100 a day, and 60 upload-link calls a minute (new links, tokens,
    complete and cancel together).

    These answers also carry next_step (what to do next, in a sentence) and most refusals retry
    ("never", or "after_reset" for a budget that frees at 00:00 UTC), because the AI connector reads the
    same answers; the schemas and the examples leave both out. The request log keeps a summary of each
    answer (ids, status, type, size and times), never the token, the upload address or the command.

    Args:
        body (UploadLinkRequest): file_id is not part of a new link (400): a fresh token for an
            unfinished upload is POST /media/uploads/{file_id}/token. Other fields are not read.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadLink | UploadLinkErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
