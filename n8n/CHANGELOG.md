# Changelog

## 0.1.0

First release.

- Credential **Status 200 Uploads API** (an API key, checked with `GET /api/v2/accounts`).
- **Post**: Create (publish now, schedule, or check only), Get, Get Many, Cancel.
- **Account**: Get Many, Get Posting Options.
- **Media**: Import From URL (waits until the file is ready), Get.
- An automatic `Idempotency-Key` on every post and media import. The node's own resends send the very
  request they repeat, and n8n's Retry On Fail sends the same key, so a lost answer is not posted twice
  (keep `$now` and random values out of the node's fields).
- Waits and sends again only what the API's retry table allows (`components.x-status200-retry` of the
  OpenAPI file): media still importing, a key still in use, a rate limit within Max Wait, and the
  short "nothing was sent" answers.
