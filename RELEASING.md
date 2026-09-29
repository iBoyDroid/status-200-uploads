# Releasing

How a new version of either package reaches npm or PyPI. Nothing is ever published from a computer:
you push a version tag, GitHub Actions checks everything again, and then waits for your approval
before it publishes.

| Tag | Workflow | Publishes | Waits for approval in |
|---|---|---|---|
| `n8n-vX.Y.Z` | [`publish-n8n.yml`](.github/workflows/publish-n8n.yml) | npm: `@status200uploads/n8n-nodes-status200uploads` | environment **npm** |
| `python-vX.Y.Z` | [`publish-python.yml`](.github/workflows/publish-python.yml) | PyPI: `status200uploads` | environment **pypi** |

Each run stops before publishing when the tag does not match the version in the package's files, or
when the tagged commit is not on `main`. A version number can be published only once, on npm and on
PyPI alike: to fix a release, publish the next version.

## One-time setup

Already done on GitHub: the repository is public; the environments **npm** (tags `n8n-v*`) and
**pypi** (tags `python-v*`) exist, with you as the required reviewer; secret scanning and push
protection are on.

Optional, a few more clicks on GitHub that nothing here depends on:

- **Settings**, **Actions**, **General**: tick **Require actions to be pinned to a full-length commit
  SHA**. Every workflow here already is.
- **Settings**, **Rules**, **Rulesets**, **New tag ruleset**: target the tag patterns `n8n-v*` and
  `python-v*`, turn on **Restrict creations**, **Restrict updates** and **Restrict deletions**, and add
  **Repository admin** to the bypass list, so that only you can make a release tag.

### PyPI (before the first Python release)

1. On pypi.org, signed in as **iBoyDroid** (your email must be verified), open **Your account**,
   **Publishing**, **Add a new pending publisher**, tab **GitHub**, and fill in:
   - PyPI Project Name: `status200uploads`
   - Owner: `iBoyDroid`
   - Repository name: `status-200-uploads`
   - Workflow name: `publish-python.yml`
   - Environment name: `pypi`
2. Click **Add**. This does not reserve the name, so release the first version soon after.

No token or password is needed, now or later: PyPI trusts this workflow directly.

### npm (for the first n8n release only)

npm can trust this workflow directly too, but only for a package that already exists on npm. The
very first version is therefore published with a short-lived token, once.

1. On npmjs.com, signed in as **iboydroid** (two-factor on, owner of the **status200uploads**
   organization), open your picture, **Access Tokens**, **Generate New Token**, **Granular Access
   Token**:
   - Token name: `status-200-uploads first publish`
   - Bypass two-factor authentication: ticked (the workflow cannot type a code)
   - Packages and scopes: **Read and write**, **Only select packages and scopes**, `@status200uploads`
   - Organizations: **No access**
   - Expiration: 7 days
   Then **Generate token** and copy it.
2. On GitHub: the repository's **Settings**, **Environments**, **npm**, **Add environment secret**.
   Name: `NPM_TOKEN`. Paste the token and save. Never paste it anywhere else or send it to anyone.

npm stops accepting such tokens for publishing in January 2027, so do the first release before then.

## Releasing the n8n node

Never run `npm run release` in `n8n/`. It is the n8n template's local release tool: from your computer
it commits, makes a tag without the `n8n-v` prefix, pushes to `main` and creates a GitHub release. Tag
by hand as below.

1. Set the new version, the same everywhere:
   - in `n8n/`, run `npm version X.Y.Z --no-git-tag-version` (it updates `package.json` and
     `package-lock.json`);
   - `PACKAGE_VERSION` in `n8n/nodes/Status200Uploads/shared/constants.ts` (it is the User-Agent);
   - a `## X.Y.Z` section at the top of `n8n/CHANGELOG.md`, and the line under **Version history** in
     `n8n/README.md`.

   The tests fail if these disagree.
2. Commit to `main`, push, and wait until **CI** is green.
3. Tag that commit and push the tag:

   ```sh
   git tag n8n-vX.Y.Z
   git push origin n8n-vX.Y.Z
   ```

4. On GitHub, open **Actions**, the run **Publish n8n node**. When **Check and pack** is green, click
   **Review deployments**, tick **npm**, and **Approve and deploy**.
5. The last job, **n8n security scan of the published version**, must turn green: it is the scan n8n's
   own review runs. The package page on npmjs.com shows the provenance badge.

### Right after the very first npm release

1. On npmjs.com, open the package `@status200uploads/n8n-nodes-status200uploads`, **Settings**,
   **Trusted Publisher**, **GitHub Actions**, and fill in:
   - Organization or user: `iBoyDroid`
   - Repository: `status-200-uploads`
   - Workflow filename: `publish-n8n.yml`
   - Environment name: `npm`
   Save, and enter your two-factor code.
2. On the same page, under **Publishing access**, choose **Require two-factor authentication and
   disallow tokens**, and save.
3. Delete the token: on npmjs.com (**Access Tokens**, delete `status-200-uploads first publish`) and on
   GitHub (**Settings**, **Environments**, **npm**, remove `NPM_TOKEN`).

From then on no token exists anywhere. The next release's log says "No NPM_TOKEN secret: publishing
through npm trusted publishing (OIDC)", which proves it.

## Releasing the Python package

1. Set the new version, the same everywhere: `version` in `python/pyproject.toml`, `__version__` in
   `python/src/status200uploads/_version.py`, and a `## X.Y.Z` section at the top of
   `python/CHANGELOG.md`. The tests fail if these disagree.
2. Commit to `main`, push, and wait until **CI** is green.
3. Tag that commit and push the tag:

   ```sh
   git tag python-vX.Y.Z
   git push origin python-vX.Y.Z
   ```

4. On GitHub, open **Actions**, the run **Publish Python package**. When **Check and build** is green,
   click **Review deployments**, tick **pypi**, and **Approve and deploy**.
5. pypi.org/project/status200uploads shows the new version, with **Verified details** and the
   attestations of this repository.

## When something goes wrong

- **A check failed before the approval**: nothing was published. Fix it on `main`, delete the tag
  (`git push --delete origin n8n-vX.Y.Z` and `git tag -d n8n-vX.Y.Z`, or the `python-v` one), and tag
  the fixed commit.
- **npm refused the publish**:
  - `E404` or `E401` when publishing without a token: the trusted publisher's four fields must match
    exactly (`iBoyDroid`, `status-200-uploads`, `publish-n8n.yml`, `npm`). On npmjs.com a trusted
    publisher cannot be edited: delete it and add it again.
  - "You cannot publish over the previously published versions": that version exists. Publish the
    next one.
- **PyPI refused the publish** ("invalid-publisher"): the pending or trusted publisher's fields must
  match exactly (`status200uploads`, `iBoyDroid`, `status-200-uploads`, `publish-python.yml`, `pypi`).
- **The scan failed after publishing**: the version is on npm, but n8n's review would refuse it. Fix
  what the scan says and release the next version.
- **The scan says the registry does not serve the version yet**: it was not scanned. npm can take
  several minutes to serve a new package everywhere. Open the run, **Re-run jobs**, **Re-run failed
  jobs**: only the scan runs again, and nothing is published twice.
- Renaming a workflow file or an environment breaks publishing until the npm and PyPI settings above are
  changed to match.
- Only approve runs you started yourself.

## The API description

`openapi/openapi.yaml` is a copy of https://status200uploads.com/openapi.yaml, never edited here. Both
packages are tested against it, and the Python client is generated from it.

When the API changes:

1. Copy the new published file over `openapi/openapi.yaml`, byte for byte with LF line endings: the
   daily comparison below expects exactly the live file.
2. Regenerate the Python client: `pip install -r python/tools/requirements.txt`, then
   `bash scripts/regenerate-python.sh`.
3. Run both test suites (`npm test` in `n8n/`, `python -m pytest` in `python/`), commit, and push.
4. If a package's behaviour changes, release a new version of it as above.

The workflow **OpenAPI copy is current** compares the copy with the live file every day and fails, which
GitHub emails you about, when they differ.
