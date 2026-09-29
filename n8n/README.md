# Status 200 Uploads node for n8n

Publish and schedule posts to **TikTok, Instagram, Facebook, YouTube, X, LinkedIn, Pinterest, Threads
and Skool** from your n8n workflows with [Status 200 Uploads](https://status200uploads.com).

This is an n8n community node. It calls the Status 200 Uploads API
(`https://status200uploads.com/api/v2`, described in [OpenAPI 3.1](https://status200uploads.com/openapi.yaml))
with your API key.

- [Installation](#installation)
- [Credentials](#credentials)
- [Operations](#operations)
- [Usage](#usage)
- [Example workflow](#example-workflow)
- [Safe retries](#safe-retries)
- [Waits and limits](#waits-and-limits)
- [Compatibility](#compatibility)
- [Resources](#resources)
- [Version history](#version-history)

## Installation

**Self-hosted n8n:** open **Settings**, **Community Nodes**, **Install**, enter
`@status200uploads/n8n-nodes-status200uploads`, and confirm. See n8n's
[community nodes installation guide](https://docs.n8n.io/integrations/community-nodes/installation-and-management/gui-installation).
In queue mode, install it with npm in `~/.n8n/nodes` instead
([manual installation](https://docs.n8n.io/integrations/community-nodes/installation-and-management/manual-installation)).

**n8n Cloud:** community nodes appear there only after n8n has verified them. Until then, use the HTTP
Request node as described in the [n8n guide](https://status200uploads.com/docs/api#guide-n8n).

## Credentials

1. In your Status 200 Uploads dashboard, open **API** and create an API key (it starts with `rl_`).
2. In n8n, create a **Status 200 Uploads API** credential and paste the key into **API Key**.
3. Save. n8n checks the key with `GET /api/v2/accounts`; a key that is deleted or switched off is refused.

The key is sent as `Authorization: Bearer <key>` and is kept in n8n's encrypted credentials. Anyone
with it can post as you: never put it in a workflow's fields or share it. More in the
[authentication docs](https://status200uploads.com/docs/api#authentication).

## Operations

| Resource | Operation | What it does |
|---|---|---|
| Post | Create | Publish a post now, schedule it (**When: At a Set Time**), or only check it (**Check Only (Dry Run)**) |
| Post | Get | Read a post or a scheduled post: status, permalink, and for a scheduled post what each network did |
| Post | Get Many | List your posts and scheduled posts, newest first, with filters |
| Post | Cancel | Stop a scheduled or queued post that has not gone out |
| Account | Get Many | Your profiles and their connected networks |
| Account | Get Posting Options | What a profile may do on each network: TikTok privacy levels, Pinterest boards, Skool groups, the Instagram limit |
| Media | Import From URL | Import an image or a video from a public URL, and wait until it is ready |
| Media | Get | Read how an import is going |

The node can also be used as a tool by n8n's AI Agent.

## Usage

**One network per node.** A Post: Create sends one post to one network from one profile. To cross-post,
use one node per network (see the example below).

**Account.** Choose it from the list, or give its ID or its `@handle`. The list comes from Account:
Get Many.

**What each network needs.**

| Network | Needs | Notes |
|---|---|---|
| TikTok | a **Privacy Level** (the list shows only the levels this account allows) and media | Photo title and description, comments, Duet, Stitch, branded content and AI label are under TikTok Options |
| YouTube | a **Privacy Status** and a video | Title, description, tags, category and the rest are under YouTube Options |
| Pinterest | a **Board** (the list comes from the account) and an image | |
| Skool | a **Group** and a **Title** | A group that needs a category takes a Label ID under Skool Options |
| Instagram | media | Post type (feed image, Reel, story, carousel) under Instagram Options |
| X, LinkedIn, Threads, Facebook | nothing more | Text posts need no media |

Option fields the node does not show yet can be sent in **Options, Additional Post Fields** as JSON,
for example `{"tiktok": {"isAiGenerated": true}}`. The fields are those of the
[OpenAPI file](https://status200uploads.com/openapi.yaml) (`components.schemas.Post`).

**Media is sent by URL.** Give public URLs of the files (one per line), or import a file first with
Media: Import From URL and send its **File ID**. Importing first suits large videos: the import can take
longer than one request. A file from an earlier node (binary data) must first be stored at a public URL
(for example S3, a Google Drive or Dropbox share, or Cloudinary). URLs that need a sign-in, or private
addresses, cannot be fetched.

**Scheduling.** Set **When** to **At a Set Time** and pick **Scheduled For**, up to 365 days ahead. A
date and time without a time zone (what the date picker stores) is read in the workflow's time zone
(its settings) and sent in UTC. The answer is `202` with `code: "scheduled"` and a `scheduled_post_id`,
which Post: Cancel stops.

**Checking a post.** With **Options, Check Only (Dry Run)** on, the API runs every check a publish makes
and sends nothing; the output is a report (`dry_run: true`, `outcome`, `reason`, `checks`).

**What comes out.** Post: Create outputs the API's answer. `status200.post_id` and
`status200.status_url` name the post in your History (use them with Post: Get). TikTok and Instagram
finish after the answer (`data.status: "processing"`); YouTube uploads and large videos answer `202`;
a network slower than the request answers `202` with `code: "still_publishing"`. None of these is a
failure, and the node never sends them again. When the answer is the stored first answer of the same
request (see [Safe retries](#safe-retries)), the output carries `replayed: true`.

**When something is refused**, the node stops with the API's own message, a line saying how to change
it, the facts of the refusal (for example when an allowance comes back) and the code, such as
`monthly_limit_reached` or `pinterest_board_required`. With the node's **On Error** setting at
*Continue*, the item carries that error and the next items go on.

To wait until a post is live, follow Post: Create with Post: Get (Post **By ID**:
`{{ $('Publish to X').item.json.status200.post_id }}`, naming the Create node, because on the next pass
the input is Post: Get's own output), then an IF on `{{ $json.done || $runIndex >= 20 }}`: true goes on,
false goes to a Wait node of 30 seconds that leads back to Post: Get. That reads the post every 30
seconds for up to 10 minutes and never sends it again.

## Example workflow

Post the same text to X and LinkedIn. Import it (**Workflows, Import from File or URL**, or paste it into
the canvas), choose your credential and your account in both Status 200 Uploads nodes, and run it.

```json
{
  "name": "Post the same text to X and LinkedIn",
  "nodes": [
    {
      "parameters": {},
      "name": "When clicking Execute workflow",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [0, 0]
    },
    {
      "parameters": {
        "account": { "__rl": true, "mode": "list", "value": "" },
        "platform": "x",
        "text": "Our new guide is out: https://example.com/guide"
      },
      "name": "Publish to X",
      "type": "@status200uploads/n8n-nodes-status200uploads.status200Uploads",
      "typeVersion": 1,
      "position": [240, -100]
    },
    {
      "parameters": {
        "account": { "__rl": true, "mode": "list", "value": "" },
        "platform": "linkedin",
        "text": "Our new guide is out: https://example.com/guide"
      },
      "name": "Publish to LinkedIn",
      "type": "@status200uploads/n8n-nodes-status200uploads.status200Uploads",
      "typeVersion": 1,
      "position": [240, 100]
    }
  ],
  "connections": {
    "When clicking Execute workflow": {
      "main": [[
        { "node": "Publish to X", "type": "main", "index": 0 },
        { "node": "Publish to LinkedIn", "type": "main", "index": 0 }
      ]]
    }
  }
}
```

More examples: a short video to TikTok, Instagram Reels and YouTube Shorts is Media: Import From URL
followed by three Post: Create nodes that send its `file_id`; a scheduled post from a sheet row is Post:
Create with **When: At a Set Time** and **Scheduled For** set to the row's date.

Two complete workflows to import are in the repository's
[templates folder](https://github.com/iBoyDroid/status-200-uploads/tree/main/n8n/templates): one
cross-posts text and an image to X, LinkedIn and Facebook; the other posts a short video to TikTok,
Instagram Reels and YouTube Shorts (or only checks it, or schedules it) and waits until each network is
done.

## Safe retries

Every Post: Create and Media: Import From URL carries an `Idempotency-Key`. The API answers the same
key with the same request, within 24 hours, with its first answer instead of doing it twice.

- **Automatic** (the default): the key is made from the workflow, the execution, the node, the item and
  the request. When the node sends a request again itself, it sends the very request it sent first, same
  body and same key. n8n's **Retry On Fail** runs the node again in the same execution, so it sends the
  same key too, and a post whose answer was lost is not posted twice. Turn Retry On Fail on for network
  drops.
- **Custom**: your own key, for example `{{ $json.guid }}-tiktok` from an RSS item, to dedupe across
  executions too. Never build it from `$now` or a random value.
- **Off**: no key. A request sent twice is done twice.

Keep a post the same on every try: work out times and random values in an earlier node, not with `$now`
in this node's fields. Retry On Fail reads the fields again, so `$now` there makes a new request: with
the Automatic key it gets a new key and is posted again, and with a Custom key it is refused
(`idempotency_key_reused`).
Running the workflow again, or **Retry** on a past execution, is a new execution: with the Automatic key
it is a new post.

## Waits and limits

The node follows the API's retry table (`components.x-status200-retry` in the OpenAPI file):

| Answer | What the node does |
|---|---|
| `409 media_processing` (a file still importing), `409 idempotency_in_progress`, `429 rate_limited` | Waits as long as the API asks (`Retry-After`), then sends the identical request again, within **Max Wait** (120 seconds by default, up to 600; for Media: Import From URL it also covers the wait until the file is ready) |
| `503` "nothing was sent" answers, `502 upstream_unavailable`, `504 cancel_unconfirmed` | Waits and sends again, at most twice |
| An answer whose outcome may not be known: a `5xx` such as `server_error`, `platform_error` or `upload_worker_failed`, `no_publish_id`, or a page that is not JSON | Sends it once more only when the request carried an Idempotency-Key (a read, a cancel or a dry run always); otherwise stops and asks you to look in History first |
| No answer at all (the connection broke or timed out) to the node's first request | Stops with n8n's own connection message. With **Retry On Fail** on, n8n runs the node again with the same automatic key, which gets the first answer back if the post went through. Without it, look in History before running it again |
| No answer at all to a request the node sends itself (a resend, the next page, an import status read) | Treated like a page that is not JSON: sent once more only with an Idempotency-Key (a read always) |
| Any `202` | A success: never sent again |
| Every other refusal (a used-up allowance, a missing field, a key used for another request) | Stops at once with the message and the fix |

Turn **Options, Wait When Asked** off to stop instead of waiting. Waiting counts toward n8n's execution
time.

API limits to plan for: one post per network every 20 seconds per account, one media import every 20
seconds, 60 reads a minute per account (the dropdowns, Get and Get Many included), and 10 posting-option
reads a minute. To send many items to the same network, space them with **Request Options, Batching**
(for example 1 item every 20 seconds). Your plan's daily and monthly allowances apply; a post over the
daily allowance is queued for the next day (`202 queued_for_next_day`).

## Compatibility

For self-hosted n8n 2.x. Built with n8n's node CLI 0.49.1 against n8n-workflow 2.40; older n8n versions
are not tested. It has no runtime dependencies.

## Resources

- [Status 200 Uploads API documentation](https://status200uploads.com/docs/api), and its
  [n8n guide](https://status200uploads.com/docs/api#guide-n8n)
- [OpenAPI 3.1 description](https://status200uploads.com/openapi.yaml)
- [n8n community nodes documentation](https://docs.n8n.io/integrations/community-nodes)
- Support: https://status200uploads.com/support or info@status200uploads.com
- Source and issues: https://github.com/iBoyDroid/status-200-uploads (folder `n8n`); security reports
  go to info@status200uploads.com, see [SECURITY.md](https://github.com/iBoyDroid/status-200-uploads/blob/main/SECURITY.md)

## Version history

See [CHANGELOG.md](CHANGELOG.md).

- **0.1.1**: no change to the node; released so n8n's Creator Portal checks it again.
- **0.1.0**: first release.

## License

[MIT](LICENSE.md). Maintained by [iBoyDroid](https://github.com/iBoyDroid).
