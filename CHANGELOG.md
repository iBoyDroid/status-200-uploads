# Changelog

Each package keeps its own changelog, released from its own tags:

- n8n node `@status200uploads/n8n-nodes-status200uploads`: [n8n/CHANGELOG.md](n8n/CHANGELOG.md)
  (tags `n8n-vX.Y.Z`)
- Python package `status200uploads`: [python/CHANGELOG.md](python/CHANGELOG.md) (tags
  `python-vX.Y.Z`)

This file records what changes in the repository around them.

## Unreleased

The first public version of the repository:

- `openapi/openapi.yaml`, the copy of https://status200uploads.com/openapi.yaml both packages are
  tested against, and a daily check that it is still the live file.
- The n8n node 0.1.0 and the Python package 0.1.0.
- Two n8n workflow templates in `n8n/templates/`: a cross-post of text and an image to X, LinkedIn and
  Facebook, and a short video to TikTok, Instagram Reels and YouTube Shorts that waits until each
  network is done.
- CI on every push and pull request, and release workflows that publish from version tags after the
  maintainer's approval, with npm provenance and PyPI attestations ([RELEASING.md](RELEASING.md)).
- `credentials/`: an exact copy of `n8n/credentials/` at the top of the repository, where n8n's
  Creator Portal looks for the node's credential; CI fails if the two differ. The n8n node 0.1.1.
