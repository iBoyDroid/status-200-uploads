# Changelog

## 0.1.1

No change to how the node works. The User-Agent now says 0.1.1.

- The repository also holds the credential at `credentials/` at its top level, where n8n's Creator
  Portal looks for it when it checks the node for verification. It is released as a new version
  because the Portal checks a node again only when npm has a new version.

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
