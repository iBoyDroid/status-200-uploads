# Changelog

## 0.1.0

First release.

- `Status200`, the client: `publish()` (now, scheduled, or a dry run with `validate()`), `wait_for()`,
  `get_post()`, `list_posts()`, `iter_posts()`, `cancel()`, `list_accounts()`,
  `get_posting_options()`, `import_media()`, `get_media()` and `wait_for_media()`.
- An automatic `Idempotency-Key` on every post and media import, reused with the byte-identical body
  on every try, so a retry never posts twice. Your own key, or none, on request.
- Waits and sends again only what the API's retry table allows (`components.x-status200-retry` of the
  OpenAPI file): media still importing, a key still in use, a rate limit within `max_wait`, and the
  short "nothing was sent" answers; an answer whose outcome is not known is sent once more only with
  a key. Every `202` is a success.
- `Status200Error` with the API's code, message and facts; `OutcomeUnknown` when a post may have gone
  through.
- The API key from `STATUS200_API_KEY` or the constructor, never shown in a repr, a log or an error.
  A 120-second timeout and a `status200uploads-python/0.1.0` User-Agent.
- `status200uploads.models` and `status200uploads.api`: the typed client generated from the OpenAPI
  file with openapi-python-client 0.29.1.
