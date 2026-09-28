"""Status 200 Uploads: publish and schedule posts to TikTok, Instagram, Facebook, YouTube, X,
LinkedIn, Pinterest, Threads and Skool.

    from status200uploads import Status200

    s200 = Status200()  # the API key from STATUS200_API_KEY
    result = s200.publish({"accountId": "@myprofile", "platform": "linkedin",
                           "content": {"text": "Hello from Python"}})

Status200 is the client to use: it sends an Idempotency-Key with every post, waits and sends again
only what the API's retry table allows, and follows a post to its result. status200uploads.models
and status200uploads.api are the typed layer generated from the API's OpenAPI file.
Documentation: https://status200uploads.com/docs/api#guide-python
"""

import logging

from ._client import API_KEY_ENV, DEFAULT_BASE_URL, USER_AGENT, Status200
from ._result import Result, Status200Ids
from ._retry import RETRY_TABLE, retry_rule
from ._version import __version__
from .errors import OutcomeUnknown, Status200Error

logging.getLogger("status200uploads").addHandler(logging.NullHandler())

__all__ = [
    "API_KEY_ENV",
    "DEFAULT_BASE_URL",
    "RETRY_TABLE",
    "USER_AGENT",
    "OutcomeUnknown",
    "Result",
    "Status200",
    "Status200Error",
    "Status200Ids",
    "__version__",
    "retry_rule",
]
