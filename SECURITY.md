# Security policy

## Reporting a vulnerability

Please do not open a public issue for a security problem. Email
**info@status200uploads.com** with what you found and how to reproduce it. You will get an answer
within a few working days, and a note when it is fixed.

This covers the code in this repository (the n8n node, the Python package, the workflows that publish
them) and the Status 200 Uploads API they call.

## Your API key

- Never paste an API key (`rl_...`) into an issue, a pull request, a log or a shared workflow. If one
  was exposed, delete it at once in your Status 200 Uploads dashboard under **API** and create a new one.
- The n8n node keeps the key in n8n's encrypted credentials. The Python package reads it from the
  `STATUS200_API_KEY` environment variable or from your code; it never writes it anywhere.

## How the packages are published

Both packages are built and published only by GitHub Actions in this repository, from a version tag,
after the maintainer approves the release. The npm package carries a provenance statement and the
PyPI package carries attestations, so anyone can check that a release was built from this repository.
