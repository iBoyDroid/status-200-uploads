import type { IDataObject } from 'n8n-workflow';
import type { Answer } from './answer';
import type { FailReason, Settled } from './retry';

/**
 * The node's own "how to change it" line per code. REST refusals carry code and message only (and
 * upgrade_url on a plan refusal); next_step and retry exist only in the AI connector, so the node
 * supplies this text. test/contract.test.ts checks that every code the OpenAPI file lists for the
 * requests this node sends has a line here.
 */
export const FIX_TEXT: Record<string, string> = {
	// 400
	bad_request: 'Change what the message names, then send it again.',
	api_error:
		'Read the message: it names what to change. A network that is not connected is connected again on the Connections page of your dashboard.',
	scheduled_for_invalid:
		'Use a date and time with a time zone, at most 365 days ahead (for example 2026-10-01T09:00:00Z). A date picked in the editor gets the workflow time zone.',
	youtube_tags_too_long: 'Remove some YouTube tags: YouTube allows 500 characters of tags in all.',
	idempotency_key_invalid:
		'Use 1 to 255 printable ASCII characters as the Custom Idempotency Key, or set Idempotency Key to Automatic.',
	profile_name_ambiguous:
		'Two of your profiles have this name in different capital letters. Choose the account from the list, or use its ID.',
	pinterest_board_required:
		'Choose a Pinterest board. The list comes from Account: Get Posting Options for this profile.',
	media_wrong_for_post_type:
		'Send media that fits the post type (a video for a Reel, for example), or change the post type.',
	options_outside_post: 'Put network options inside the post: check Additional Post Fields.',
	media_not_available:
		'The media URL could not be fetched. Use a public URL of the file itself that opens without signing in.',
	video_size_unknown:
		'The size of the video could not be read from its URL. Import it with Media: Import From URL and send its file ID.',
	no_container:
		'Instagram did not take the media. Check that it fits Instagram rules (format, size, length), then send it again.',
	no_publish_id:
		'TikTok did not confirm the upload. Look for the post in History (Post: Get Many) before sending it again.',
	pinterest_sandbox_board:
		'This board belongs to a Pinterest test connection. Reconnect Pinterest on the Connections page and choose a real board.',
	pinterest_rejected:
		'Pinterest refused the pin, for the reason in the message. Change what it names, then send it again.',
	x_rejected:
		'X refused the post, for the reason in the message. Change what it names (or reconnect X on the Connections page), then send it again.',
	skool_rejected:
		'Skool refused the post, for the reason in the message. Change what it names, then send it again.',
	category_required: 'This Skool group needs a category: set Label ID under Skool Options.',
	// 401
	unauthorized:
		'Check the API key in the credential of this node. If it was deleted or switched off, create a new one in your Status 200 Uploads dashboard under API.',
	reconnect_required:
		'The network no longer accepts the sign-in of this profile. Reconnect it on the Connections page of your dashboard, then send the post again.',
	RECONNECT_REQUIRED:
		'Instagram no longer accepts the sign-in of this profile. Reconnect it on the Connections page of your dashboard, then send the post again.',
	REFRESH_TOKEN_EXPIRED:
		'TikTok no longer accepts the sign-in of this profile. Reconnect it on the Connections page of your dashboard, then send the post again.',
	NO_TOKEN:
		'This network has no sign-in for the profile. Connect it on the Connections page of your dashboard, then send the post again.',
	TOKEN_REFRESH_FAILED:
		'The sign-in of the network could not be renewed just now. Try again later, and reconnect the network if it keeps happening.',
	pinterest_auth_failed:
		'Pinterest no longer accepts the sign-in of this profile. Reconnect it on the Connections page of your dashboard, then send the pin again.',
	// 403
	account_not_found:
		'No profile with this name or ID on your account. Choose the account from the list (your profiles are named below).',
	plan_required:
		'Your plan does not include this network. Upgrade at the address below, or post to another network.',
	forbidden: 'The network refused this for the profile, for the reason in the message.',
	// 404
	media_not_found:
		'No imported file with this ID on your account. Import the file again with Media: Import From URL (files are kept for 7 days).',
	post_not_found: 'No post or scheduled post with this ID on your account.',
	not_found: 'This address is not an endpoint of the API. Update the node to its latest version.',
	// 405
	method_not_allowed:
		'This address does not take this method. Update the node to its latest version.',
	// 409
	media_processing:
		'The file is still importing. Turn on Wait When Asked (under Options) or raise Max Wait, or send the post again later.',
	scheduled_queue_full:
		'You have 500 posts waiting. Cancel some with Post: Cancel, or wait until some have gone out.',
	idempotency_in_progress:
		'The first request with this Idempotency-Key is still running. Send it again in a few seconds (the node does, when Wait When Asked is on).',
	idempotency_outcome_unknown:
		'The first request with this Idempotency-Key never answered. Look for the post in History (Post: Get Many), and send it again with a new key only if it is not there.',
	not_cancellable:
		'It can no longer be cancelled: it is being published, was published, or did not go out (its status is below).',
	// 413
	MEDIA_TOO_LARGE:
		'The file is larger than this network accepts. Send a smaller file (the limits are at the address below).',
	// 422
	media_failed:
		'The import of this file did not finish. Import it again with Media: Import From URL.',
	idempotency_key_reused:
		'This Idempotency-Key was used in the last 24 hours for a different request. Keep the request the same on every try (no $now in its fields), or use a new key.',
	photo_format_not_supported:
		'TikTok takes photos as JPEG or WebP, and this photo could not be converted. Send a JPEG.',
	photo_too_large_to_convert: 'The photo is too large to convert for TikTok. Send a smaller JPEG.',
	photo_conversion_failed: 'The photo could not be converted for TikTok. Send it as a JPEG.',
	// 429
	rate_limited:
		'Too many requests in a short time: one post per network every 20 seconds per account, one import every 20 seconds, 60 reads a minute. Space the items out (Batching under Request Options) or raise Max Wait.',
	monthly_limit_reached:
		'The monthly allowance of your plan is used up. It comes back at the time below; upgrade to post now.',
	daily_limit_reached:
		'The daily allowance of your plan is used up. It comes back at the time below.',
	x_limit_reached:
		'The posts of your X add-on are used up for now. They come back at the time below.',
	x_link_limit_reached:
		'The posts with links of your X add-on are used up for now. Post without a link, or wait until the time below.',
	daily_attempts_exceeded: 'Too many attempts today for this profile. Try again after 00:00 UTC.',
	import_budget_exhausted:
		'The import allowance of this key is used up. It comes back at the time below.',
	// 5xx
	server_error:
		'Status 200 Uploads could not finish this request. Look for the post in History (Post: Get Many) before sending it again.',
	platform_error:
		'The network could not take the post, for the reason in the message. Look for it in History (Post: Get Many) before sending it again.',
	upstream_unavailable:
		'The request never reached Status 200 Uploads, and nothing was posted. Send it again.',
	upload_worker_failed:
		'The upload of the video to the network stopped. Look for the post in History (Post: Get Many) before sending it again.',
	caller_check_unavailable:
		'Nothing was posted: a check could not run just now. Send it again in a few seconds.',
	schedule_check_unavailable:
		'Nothing was scheduled: a check could not run just now. Send it again in a few seconds.',
	idempotency_unavailable:
		'Nothing was sent: the Idempotency-Key could not be checked just now. Send it again in a few seconds.',
	dry_run_unavailable: 'The check could not run just now. Send it again in a few seconds.',
	skool_unavailable:
		'Skool is not taking posts from Status 200 Uploads right now. Try again later.',
	x_unavailable: 'X is not taking posts from Status 200 Uploads right now. Try again later.',
	cancel_unconfirmed:
		'The cancel did not answer in time. Send the same cancel again: cancelling twice is safe.',
};

/** The line for an answer without a code of its own, by its status. */
export function fixForStatus(status: number, media: boolean): string {
	if (status === 0) return 'No answer arrived: the connection broke or timed out.';
	if (media && status === 400) {
		return 'Check that the URL is a public http or https link to the image or video file itself.';
	}
	if (status === 400) return 'Change what the message names, then send it again.';
	if (status === 401) return FIX_TEXT.unauthorized;
	if (status === 403) return 'This is not allowed for this account; the message says why.';
	if (status === 404) return 'Nothing was found with this ID on your account.';
	if (status === 405) return FIX_TEXT.method_not_allowed;
	if (status === 409)
		return 'Another request with this key is still running. Send it again in a few seconds.';
	if (status === 413) return 'The file is too large: images up to 20 MB, videos up to 5 GB.';
	if (status === 415)
		return 'The URL must return an image or a video file, not a web page that shows it.';
	if (status === 422) return 'This cannot be done as it is; the message says why.';
	if (status === 429) return FIX_TEXT.rate_limited;
	if (status >= 500) return 'Status 200 Uploads or the network could not finish this request.';
	return 'Read the message for what to change.';
}

/** What kind of request it was: the advice for an unknown outcome depends on it. */
export type RequestKind = 'post' | 'media' | 'read';

function reasonLine(settled: Settled, kind: RequestKind, maxWaitSeconds: number): string {
	const reason: FailReason | undefined = settled.reason;
	const asked = settled.askedWaitSeconds ?? 0;
	const check =
		kind === 'post'
			? 'Look for the post in History (Post: Get Many) before sending it again.'
			: kind === 'media'
				? 'Import the file again if it is needed.'
				: 'Send it again.';
	switch (reason) {
		case 'wait_off':
			return `The API asked to wait ${asked} seconds and send the same request again; Wait When Asked is off, so the node did not.`;
		case 'max_wait':
			return `The API asks to wait ${asked} more seconds, which would pass Max Wait (${maxWaitSeconds} seconds in all). Raise Max Wait, or send it again later.`;
		case 'tries_used':
			return `Sent ${settled.sends} times, and the answer did not change.`;
		case 'no_key':
			return `The outcome is not known, and without an Idempotency-Key the node does not send it again. ${check}`;
		case 'once_used':
			return `Sent once more with the same Idempotency-Key, and the outcome is still not known. ${check}`;
		default:
			return '';
	}
}

function factsOf(answer: Answer): string[] {
	const error = answer.body?.error;
	const e: IDataObject =
		typeof error === 'object' && error !== null && !Array.isArray(error)
			? (error as IDataObject)
			: (answer.body ?? {});
	const facts: string[] = [];
	const text = (v: unknown): string | undefined =>
		typeof v === 'string' && v !== '' ? v : typeof v === 'number' ? String(v) : undefined;
	if (text(e.reason)) facts.push(`Reason: ${text(e.reason)}.`);
	if (text(e.status) && answer.code === 'not_cancellable') facts.push(`Status: ${text(e.status)}.`);
	if (text(e.resets_at)) facts.push(`Comes back at ${text(e.resets_at)}.`);
	if (text(e.file_id)) facts.push(`File ID: ${text(e.file_id)}.`);
	if (Array.isArray(e.profiles) && e.profiles.length > 0) {
		facts.push(
			`Your profiles: ${e.profiles.slice(0, 10).map(String).join(', ')}${e.profiles.length > 10 ? ' ...' : ''}.`,
		);
	}
	if (text(e.limits_url)) facts.push(`Limits: ${text(e.limits_url)}`);
	if (text(e.upgrade_url)) facts.push(`Upgrade: ${text(e.upgrade_url)}`);
	return facts;
}

/**
 * The description of a failed answer: why the node stopped (when it was the node's choice), how to
 * change it, the facts of the refusal, and its code.
 */
export function describeFailure(
	settled: Settled,
	kind: RequestKind,
	maxWaitSeconds: number,
): string {
	const answer = settled.answer;
	const fix =
		(answer.code && FIX_TEXT[answer.code]) || fixForStatus(answer.status, kind === 'media');
	const parts = [reasonLine(settled, kind, maxWaitSeconds), fix, ...factsOf(answer)].filter(
		(p) => p !== '',
	);
	const tag = answer.status === 0 ? 'no answer' : `HTTP ${answer.status}`;
	parts.push(answer.code ? `(${tag}, code ${answer.code})` : `(${tag})`);
	return parts.join(' ');
}

/** The message of a failed answer: the API's own words, else what happened. */
export function failureMessage(answer: Answer): string {
	if (answer.message) return answer.message;
	if (answer.status === 0)
		return `No answer from Status 200 Uploads${answer.text ? ` (${answer.text})` : ''}`;
	if (!answer.json)
		return `Status 200 Uploads answered HTTP ${answer.status} with a page that is not JSON`;
	return `Status 200 Uploads answered HTTP ${answer.status}`;
}
