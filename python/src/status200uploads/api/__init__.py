"""The API's operations, generated from its OpenAPI file: one module per operation, each with
sync(), sync_detailed(), asyncio() and asyncio_detailed(). Pass them ``client=s200.client``.

    from status200uploads import Status200
    from status200uploads.api.accounts import list_accounts

    s200 = Status200()
    accounts = list_accounts.sync(client=s200.client)

They send each request exactly once, as it is: no Idempotency-Key unless you pass one, no waits,
no retries (Status200 adds those), and an answer that is not JSON raises json.JSONDecodeError.
"""

from . import accounts, media, posts

__all__ = ["accounts", "media", "posts"]
