# Workflow templates

Two ready-made n8n workflows that use the Status 200 Uploads node. They are not part of the npm
package: import them into your own n8n.

| File | What it does |
|---|---|
| [`cross-post-x-linkedin-facebook.json`](cross-post-x-linkedin-facebook.json) | **Cross-post text and an image to X, LinkedIn and Facebook with Status 200 Uploads.** Imports one image, posts it with your text to the three networks, then reads each post back: network, status and link. |
| [`short-video-tiktok-instagram-youtube.json`](short-video-tiktok-instagram-youtube.json) | **Publish a short video to TikTok, Instagram Reels and YouTube Shorts and confirm it went live.** Imports one video and posts it to the three networks, schedules it, or only checks it; posts sent now are read every 30 seconds, for up to 10 minutes, until each network is done. |

## Before you import

1. Install the community node: in n8n, **Settings, Community Nodes, Install**, and enter
   `@status200uploads/n8n-nodes-status200uploads`. Until n8n verifies the node, this works on
   self-hosted n8n only.
2. In your [Status 200 Uploads](https://status200uploads.com) dashboard, connect the networks the
   template posts to, and create an API key on the **API** page.

## Import and set up

1. In n8n, open **Workflows**, then **Import from File**, and choose the JSON file (or open the file,
   copy everything, and paste it onto an empty canvas).
2. The templates carry no credentials. Open each Status 200 Uploads node, create or choose a
   **Status 200 Uploads API** credential with your key, and choose your **Account**.
3. In the short-video template, also choose who can see the video in **Publish to TikTok** (the list
   shows the levels your TikTok account allows). **Publish to YouTube Shorts** posts the video as
   Private until you change **YouTube Privacy Status**.
4. Fill in **Your settings** and click **Execute workflow**.

### The short-video template's settings

| Field | Meaning |
|---|---|
| `video_url` | The public URL of the video file itself (MP4, MOV or WebM, up to 5 GB) |
| `caption` | The text of the post on every network (the description on YouTube) |
| `youtube_title` | The YouTube title, up to 100 characters |
| `check_only` | `true` (as shipped): the API runs every check a post makes and posts nothing (the video is still imported, so the checks can see it; imports are kept for 7 days). Set it to `false` to post. |
| `publish_at` | Empty: post now. A date and time such as `2026-10-01 09:00` schedules the posts, read in the workflow's time zone (its settings), or give a time zone yourself, such as `2026-10-01T09:00:00+02:00`. |

A scheduled post is listed in the result with its `scheduled_post_id`. To stop it before it goes out,
run the node's **Post: Cancel** with that id.

## Safe to run again

Every post and import carries an automatic Idempotency-Key, made from the workflow, the execution, the
node, the item and the request. Turning on **Retry On Fail** for the Publish nodes is safe: a retry in
the same execution gets the first answer back instead of posting twice, as long as no field of those nodes
uses `$now` or a random value (a changed request is a new post). Running the whole workflow again
is a new execution, and posts again.

## Tested

`../test/templates.test.ts` checks both files against n8n's template rules (named nodes, one overview
sticky note, no credentials) and runs every Status 200 Uploads node through n8n's own expression engine,
with the example answers of the [OpenAPI file](../../openapi/openapi.yaml), to check the requests it
sends.
