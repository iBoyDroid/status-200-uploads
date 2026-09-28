# Status 200 Uploads: public packages

[Status 200 Uploads](https://status200uploads.com) publishes and schedules posts to TikTok, Instagram,
Facebook, YouTube, X, LinkedIn, Pinterest, Threads and Skool through one API. This repository holds the
open-source clients of that API.

| Folder | What it is | Install |
|---|---|---|
| [`n8n/`](n8n) | The n8n community node **Status 200 Uploads** | n8n: Settings, Community Nodes, Install `@status200uploads/n8n-nodes-status200uploads` |
| [`python/`](python) | The Python package `status200uploads` | `pip install status200uploads` |
| [`openapi/openapi.yaml`](openapi/openapi.yaml) | The OpenAPI 3.1 description of the API | Served at https://status200uploads.com/openapi.yaml |

Both packages call `https://status200uploads.com/api/v2` with an API key from your Status 200 Uploads
dashboard (**API** page), and both are tested against `openapi/openapi.yaml` and its
`components.x-status200-retry` table, which says which answers a client may send again and how.

## The API description

`openapi/openapi.yaml` is a copy of https://status200uploads.com/openapi.yaml, the file the service
publishes. It is written from the service's code and checked against its live answers; this copy is
updated when the API changes, and never edited here.

## Documentation and help

- API documentation: https://status200uploads.com/docs/api
- n8n guide: https://status200uploads.com/docs/api#guide-n8n
- Python guide: https://status200uploads.com/docs/api#guide-python
- Support: https://status200uploads.com/support, or info@status200uploads.com
- Security problems: see [SECURITY.md](SECURITY.md). Please do not open a public issue for them.

## Releases

Each package is released from its own tag (`n8n-vX.Y.Z` for the n8n node, `python-vX.Y.Z` for the
Python package) by GitHub Actions in this repository, with a provenance statement (npm) or attestations
(PyPI). Nothing is published from a personal machine.

## License

[MIT](LICENSE). Maintained by [iBoyDroid](https://github.com/iBoyDroid).
