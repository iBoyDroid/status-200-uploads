# status200uploads

Publish and schedule posts to **TikTok, Instagram, Facebook, YouTube, X, LinkedIn, Pinterest, Threads
and Skool** from Python with [Status 200 Uploads](https://status200uploads.com).

This package calls the Status 200 Uploads API (`https://status200uploads.com/api/v2`, described in
[OpenAPI 3.1](https://status200uploads.com/openapi.yaml)) with your API key. It is a typed client
generated from that file, plus a small hand-written layer that makes posting safe to retry: every post
carries an `Idempotency-Key`, and the client waits and sends again only what the API says may be sent
again.

- [Install](#install)
- [Your API key](#your-api-key)
- [Quick start](#quick-start)
- [Media, TikTok and the other networks](#media-tiktok-and-the-other-networks)
- [Scheduling](#scheduling)
- [What publish() returns](#what-publish-returns)
- [When something is refused](#when-something-is-refused)
- [Safe retries](#safe-retries)
- [Waits and limits](#waits-and-limits)
- [Reading your posts](#reading-your-posts)
- [Typed models and raw operations](#typed-models-and-raw-operations)
- [Resources](#resources)

## Install

```
pip install status200uploads
```

Python 3.11 or newer. It depends only on `httpx` and `attrs`.

## Your API key

1. In your Status 200 Uploads dashboard, open **API** and create an API key (it starts with `rl_`).
2. Put it in the `STATUS200_API_KEY` environment variable, or pass it as `Status200(api_key=...)`.

The key is sent only to the API, as `Authorization: Bearer <key>`. The client never prints it: not in
its `repr`, its logs or its errors. Anyone with the key can post as you, so keep it out of your code and
your repository. More in the [authentication docs](https://status200uploads.com/docs/api#authentication).

## Quick start

```python
from status200uploads import Status200

s200 = Status200()  # the key comes from STATUS200_API_KEY

for account in s200.list_accounts():
    print(account["handle"], [network["platform"] for network in account["networks"]])

result = s200.publish(
    {
        "accountId": "@myprofile",
        "platform": "linkedin",
        "content": {"text": "Hello from Python"},
    },
    wait=True,
)
final = result.final or {}  # None when the post could not be read back
print(final.get("status"), final.get("permalink"))
```

A post goes to one network from one profile. `accountId` is a profile's `handle` (`@name`) or its
`profile_id` from `list_accounts()`. With `wait=True` the client reads the post every 30 seconds until
the network is done (for up to 10 minutes) and puts the last read in `result.final`. If the post cannot
be read back, `result.final` stays `None` and nothing is raised: the post itself was accepted.

Use `with Status200() as s200:` (or `s200.close()`) to close the connection when you are done.

## Media, TikTok and the other networks

Media is sent by public URL: either straight in the post (`content.mediaUrls`), or imported first and
sent by its `file_id` (`content.mediaID`). Importing first suits videos, since the import can take
longer than one request.

```python
media = s200.import_media("https://example.com/video.mp4")  # waits until it is ready

profile = s200.list_accounts()[0]
options = s200.get_posting_options(profile["profile_id"], platforms=["tiktok"])
tiktok = options["networks"][0]
print(tiktok["options"]["privacy_level_options"])  # the levels this TikTok account allows

result = s200.publish(
    {
        "accountId": profile["profile_id"],
        "platform": "tiktok",
        "content": {"text": "New video", "mediaID": [media["file_id"]]},
        "tiktok": {"privacyLevel": "SELF_ONLY"},
    }
)
```

| Network | Needs | Where |
|---|---|---|
| TikTok | a privacy level the account allows, and media | `post.tiktok.privacyLevel` (see `get_posting_options()`) |
| YouTube | a video; its privacy | `post.youtube.privacyStatus` (and `title`, `tags` ...) |
| Pinterest | a board and an image | `post.pinterest.boardId` (boards from `get_posting_options()`) |
| Skool | a group and a title | `post.skool.group`, `post.skool.title` |
| Instagram | media | `post.instagram.postType` (feed image, Reel, story, carousel) |
| X, LinkedIn, Threads, Facebook | nothing more | text posts need no media |

Every field is in the [OpenAPI file](https://status200uploads.com/openapi.yaml)
(`components.schemas.Post`) and the [API docs](https://status200uploads.com/docs/api). A field the API
does not use never refuses a post: it comes back in `result.warnings`.

**Check a post first.** `s200.validate(post)` runs every check a publish makes and sends nothing. The
report says `outcome` (publish, schedule, queue or refuse), `would_publish`, `reason` and each check.

## Scheduling

```python
from datetime import datetime, timezone

post = {"accountId": "@myprofile", "platform": "x", "content": {"text": "See you on Thursday"}}
result = s200.publish(post, scheduled_for=datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc))
print(result.code)  # "scheduled"

s200.cancel(result.status200.scheduled_post_id)  # stop it before it goes out
```

`scheduled_for` takes an ISO 8601 time with a time zone (`"2026-10-01T09:00:00Z"`), a Unix time, or a
`datetime` that has a time zone. A `datetime` without one is refused before anything is sent, because
the API refuses such a time. More than 60 seconds ahead (up to 365 days) the post is scheduled; your
plan's allowance is checked when it goes out.

## What publish() returns

A `Result` for every answer that is a success:

| | |
|---|---|
| `result.status_code` | `200`: published (or a dry run's report). `202`: accepted, not published yet |
| `result.code` | the `202`'s case: `scheduled`, `queued_for_next_day` (daily allowance used up), `still_publishing` (the network is slower than the request), or `None` while `data.status` is `processing` |
| `result.status200` | our ids: `post_id`, `scheduled_post_id` and `status_url` (read it with `get_post()` or `wait_for()`) |
| `result.data` | the network's own answer (its fields differ per network) |
| `result.warnings` | fields that were not used, and other things to know |
| `result.replayed` | `True` when this is the stored first answer to the same `Idempotency-Key` |
| `result.idempotency_key` | the key the post was sent with |
| `result.raw` | the whole JSON answer |

A `202` is never a failure: the post is on its way, scheduled or queued, and it must not be sent again.
TikTok and Instagram finish after the answer (`data.status: "processing"`); `wait_for(result)` follows
them to the end.

## When something is refused

```python
from status200uploads import OutcomeUnknown, Status200Error

try:
    s200.publish(post)
except OutcomeUnknown as error:
    # No clear answer: the post may have gone through.
    print(error.message)
except Status200Error as error:
    print(error.code, error.message)  # e.g. monthly_limit_reached, and what to do
    print(error.details)  # the refusal's facts: resets_at, profiles, upgrade_url ...
```

`Status200Error` carries the API's `code` (branch on it), its `message` (a sentence for a person), the
HTTP `status`, the refusal's facts in `details`, `retry_after_seconds` when the API asked for a wait,
`reason`, which says why the client stopped (`refused`, `max_wait`, `tries_used`, `no_key`,
`once_used` or `import_failed`), and `note`, what the client did before it stopped. `str(error)` puts
the message, the note, the status and the code together.

`OutcomeUnknown` (a `Status200Error`) means the client cannot tell whether the post went through: no
answer arrived, or a page that is not JSON, or a server error, even after sending it once more. Look at
your posts (`s200.list_posts()` or History in the dashboard) before sending it again, or send it again
with the same `idempotency_key` within 24 hours, which never posts twice.

## Safe retries

Every `publish()` and `import_media()` carries an `Idempotency-Key`. The API answers the same key with
the same request, within 24 hours, with its first answer (`result.replayed` is then `True`) instead of
doing it twice.

- **Automatic** (the default): a new key for each call, reused on every try the client makes, with the
  exact same body.
- **Your own key**: `s200.publish(post, idempotency_key=f"{row_id}-linkedin")`, made from your record
  and the network. The same record then never posts twice, even from another run of your program.
  Build it from something stable, never from the time or a random value. A different post under the
  same key is refused (`idempotency_key_reused`).
- **None**: `idempotency_key=False`. An answer whose outcome is not known is then never sent again.

## Waits and limits

The client follows the API's retry table (`components.x-status200-retry` in the
[OpenAPI file](https://status200uploads.com/openapi.yaml)):

| Answer | What the client does |
|---|---|
| `409 media_processing` (a file still importing), `409 idempotency_in_progress`, `429 rate_limited` | Waits as long as the API asks (`Retry-After`), then sends the identical request again, within `max_wait` |
| `503` "nothing was sent" answers, `502 upstream_unavailable`, `504 cancel_unconfirmed` | Waits and sends again, at most twice |
| An answer whose outcome may not be known: a `5xx` such as `server_error` or `platform_error`, a page that is not JSON, or no answer at all | Sends it once more, and only with an `Idempotency-Key` (a read, a cancel or a dry run always); otherwise raises `OutcomeUnknown` |
| Any `202` | A success: never sent again |
| Every other refusal | Raises `Status200Error` at once |

`Status200(max_wait=120, max_tries=5, timeout=httpx.Timeout(120, connect=10))` are the defaults:
`max_wait` is the most the client waits in all when the API asks it to (seconds; `0` never waits, and
the error then says how long to wait), `max_tries` the most requests for one call. Each call of
`publish()` can override `max_wait` and `max_tries`.

The API's limits: one post per network every 20 seconds per account, one media import every 20
seconds, 60 reads a minute per account (`wait_for()` reads every 30 seconds), and 10 posting-option
reads a minute. Your plan's daily and monthly allowances apply; a post over the daily allowance is
queued for the next day (`202 queued_for_next_day`).

The client logs each wait at INFO on the `status200uploads` logger (never the key).

## Reading your posts

```python
page = s200.list_posts(limit=50, status=["failed"], platform="tiktok")
for post in s200.iter_posts(platform="x"):  # every page, newest first
    print(post["id"], post["status"], post.get("permalink"))

post = s200.get_post(result.status200.post_id)
final = s200.wait_for(result)  # every 30 seconds, for up to 10 minutes
```

## Typed models and raw operations

The request and answer objects of the OpenAPI file are in `status200uploads.models` (attrs classes
with `to_dict()` and `from_dict()`), and `publish()` takes them as well as dicts:

```python
from status200uploads.models import Post, PostContent

s200.publish(Post(account_id="@myprofile", platform="x", content=PostContent(text="Typed")))
```

The raw operations are in `status200uploads.api` (`posts`, `accounts`, `media`), each with `sync()`,
`sync_detailed()`, `asyncio()` and `asyncio_detailed()`. Pass them `s200.client`, which shares the key,
timeout and connection. They send each request once, exactly as given: no `Idempotency-Key` unless you
pass one, no waits and no retries.

```python
from status200uploads.api.accounts import list_accounts

answer = list_accounts.sync(client=s200.client)
```

## Resources

- [Status 200 Uploads API documentation](https://status200uploads.com/docs/api), and its
  [Python guide](https://status200uploads.com/docs/api#guide-python)
- [OpenAPI 3.1 description](https://status200uploads.com/openapi.yaml)
- Support: https://status200uploads.com/support or info@status200uploads.com
- Source and issues: https://github.com/iBoyDroid/status-200-uploads (folder `python`); security
  reports go to info@status200uploads.com, see
  [SECURITY.md](https://github.com/iBoyDroid/status-200-uploads/blob/main/SECURITY.md)
- [Changelog](https://github.com/iBoyDroid/status-200-uploads/blob/main/python/CHANGELOG.md)

### Working on this package

The code under `src/status200uploads/_generated` is generated from `openapi/openapi.yaml` and never
edited by hand:

```
pip install -r python/tools/requirements.txt
bash scripts/regenerate-python.sh
pip install -e "python[test]"
pytest python
```

## License

[MIT](https://github.com/iBoyDroid/status-200-uploads/blob/main/python/LICENSE). Maintained by
[iBoyDroid](https://github.com/iBoyDroid).
