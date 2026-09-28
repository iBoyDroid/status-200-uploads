import type { Answer } from './answer';

/**
 * What a client may do with an answer (components.x-status200-retry.rules of the OpenAPI file):
 *   wait_and_resend       nothing was sent, or the first answer comes back: wait, then send the
 *                         IDENTICAL request again (same body, same Idempotency-Key);
 *   resend_once_with_key  the outcome may not be known: send it once more only with an Idempotency-Key;
 *   never                 the same request cannot succeed now;
 *   not_a_failure         accepted: it goes out on its own.
 */
export type RetryRule = 'wait_and_resend' | 'resend_once_with_key' | 'never' | 'not_a_failure';

/**
 * A copy of components.x-status200-retry of openapi/openapi.yaml. test/contract.test.ts holds the two
 * equal, so a change of the API's table fails this package's tests until the node follows it.
 */
export const RETRY_TABLE: {
	version: number;
	by_code: Record<string, RetryRule>;
	by_status: Record<'2xx' | '4xx' | '5xx' | 'not_json', RetryRule>;
} = {
	version: 1,
	by_code: {
		media_processing: 'wait_and_resend',
		idempotency_in_progress: 'wait_and_resend',
		rate_limited: 'wait_and_resend',
		caller_check_unavailable: 'wait_and_resend',
		schedule_check_unavailable: 'wait_and_resend',
		idempotency_unavailable: 'wait_and_resend',
		dry_run_unavailable: 'wait_and_resend',
		upstream_unavailable: 'wait_and_resend',
		cancel_unconfirmed: 'wait_and_resend',
		skool_unavailable: 'wait_and_resend',
		x_unavailable: 'wait_and_resend',
		platform_error: 'resend_once_with_key',
		server_error: 'resend_once_with_key',
		upload_worker_failed: 'resend_once_with_key',
		no_publish_id: 'resend_once_with_key',
		idempotency_outcome_unknown: 'never',
		idempotency_key_reused: 'never',
		monthly_limit_reached: 'never',
		daily_limit_reached: 'never',
		daily_attempts_exceeded: 'never',
		x_limit_reached: 'never',
		x_link_limit_reached: 'never',
		import_budget_exhausted: 'never',
		scheduled: 'not_a_failure',
		queued_for_next_day: 'not_a_failure',
		still_publishing: 'not_a_failure',
		schedule_unconfirmed: 'not_a_failure',
	},
	by_status: {
		'2xx': 'not_a_failure',
		'4xx': 'never',
		'5xx': 'resend_once_with_key',
		not_json: 'resend_once_with_key',
	},
};

/**
 * The rule of an answer: by its code first, else by its status class, else the answer that is not
 * JSON (a gateway's page, or no answer at all). The same order as the OpenAPI file's reader.
 */
export function retryRuleFor(answer: Pick<Answer, 'status' | 'code' | 'json'>): RetryRule {
	if (!answer.json) return RETRY_TABLE.by_status.not_json;
	if (
		typeof answer.code === 'string' &&
		Object.prototype.hasOwnProperty.call(RETRY_TABLE.by_code, answer.code)
	) {
		return RETRY_TABLE.by_code[answer.code];
	}
	const cls = `${String(answer.status)[0]}xx`;
	if (cls === '2xx' || cls === '4xx' || cls === '5xx') return RETRY_TABLE.by_status[cls];
	return 'never';
}

/**
 * Codes that say "nothing was sent, a check could not run just now": sent again at most this many
 * times, however short the wait.
 */
export const UNAVAILABLE_CODES = new Set([
	'caller_check_unavailable',
	'schedule_check_unavailable',
	'idempotency_unavailable',
	'dry_run_unavailable',
	'upstream_unavailable',
	'cancel_unconfirmed',
	'skool_unavailable',
	'x_unavailable',
]);
export const UNAVAILABLE_RESENDS = 2;

/** The wait when an answer names none (seconds). */
export const DEFAULT_WAIT_SECONDS = 5;

/** Never more requests than this for one item, whatever the waits. */
export const MAX_SENDS = 30;

/** Why an answer ended as a failure. */
export type FailReason =
	/** The rule is never (or the answer contradicts itself). */
	| 'refused'
	/** The API asked to wait and send again, and Wait When Asked is off. */
	| 'wait_off'
	/** Waiting as asked would pass Max Wait. */
	| 'max_wait'
	/** Sent as often as allowed; the answer did not change. */
	| 'tries_used'
	/** The outcome may not be known, and without an Idempotency-Key it is not sent again. */
	| 'no_key'
	/** Sent once more with the key, and the outcome is still not known. */
	| 'once_used';

export interface Settled {
	ok: boolean;
	/** The last answer. */
	answer: Answer;
	/** The rule of the last answer. */
	rule: RetryRule;
	/** Why it failed (ok false). */
	reason?: FailReason;
	/** How many requests were sent in all, the first included. */
	sends: number;
	/** How long the node waited in all (seconds). */
	waitedSeconds: number;
	/** The wait the last answer asked for (seconds), when it asked. */
	askedWaitSeconds?: number;
}

export interface SettleOptions {
	/** Sends the identical request again: same method, URL, body and Idempotency-Key. */
	send: () => Promise<Answer>;
	/** Waits (n8n-workflow's sleep; a stub in tests). */
	sleep: (ms: number) => Promise<void>;
	/** An Idempotency-Key was on the request. */
	keySent: boolean;
	/** Sending it twice changes nothing (a read, a cancel, a dry run). */
	repeatable: boolean;
	/** Wait and send again when the API asks (Retry-After). */
	waitWhenAsked: boolean;
	/** The most the node waits in all for this request (seconds). */
	maxWaitSeconds: number;
}

/** The wait an answer asks for: Retry-After, else retry_after_seconds, else 5 seconds. */
export function askedWaitSeconds(answer: Answer): number {
	return Math.max(1, answer.retryAfterHeader ?? answer.retryAfterSeconds ?? DEFAULT_WAIT_SECONDS);
}

/**
 * Follows the retry table from the first answer to a final one: waits and sends the identical
 * request again only where the table allows it, within the caps, and says why when it stops.
 */
export async function settle(first: Answer, options: SettleOptions): Promise<Settled> {
	let answer = first;
	let sends = 1;
	let waited = 0;
	let unavailableResends = 0;
	let resentOnce = false;

	const end = (ok: boolean, rule: RetryRule, reason?: FailReason, asked?: number): Settled => ({
		ok,
		answer,
		rule,
		reason,
		sends,
		waitedSeconds: waited,
		askedWaitSeconds: asked,
	});

	for (;;) {
		const rule = retryRuleFor(answer);
		const is2xx = answer.status >= 200 && answer.status < 300;

		// A 2xx with a JSON body is never a failure (a 202 is on its way, scheduled or queued).
		if (is2xx && answer.json) return end(true, 'not_a_failure');

		if (rule === 'wait_and_resend') {
			const wait = askedWaitSeconds(answer);
			if (!options.waitWhenAsked) return end(false, rule, 'wait_off', wait);
			const unavailable = UNAVAILABLE_CODES.has(answer.code ?? '');
			if (unavailable && unavailableResends >= UNAVAILABLE_RESENDS)
				return end(false, rule, 'tries_used', wait);
			if (sends >= MAX_SENDS) return end(false, rule, 'tries_used', wait);
			if (waited + wait > options.maxWaitSeconds) return end(false, rule, 'max_wait', wait);
			if (unavailable) unavailableResends++;
			await options.sleep(wait * 1000);
			waited += wait;
			answer = await options.send();
			sends++;
			continue;
		}

		if (rule === 'resend_once_with_key') {
			if (!options.keySent && !options.repeatable) return end(false, rule, 'no_key');
			if (resentOnce) return end(false, rule, 'once_used');
			const wait = Math.max(1, answer.retryAfterHeader ?? DEFAULT_WAIT_SECONDS);
			resentOnce = true;
			await options.sleep(wait * 1000);
			waited += wait;
			answer = await options.send();
			sends++;
			continue;
		}

		// never, or not_a_failure on an answer that is not a 2xx (it contradicts itself).
		return end(false, rule, 'refused');
	}
}
