import { describe, expect, it } from 'vitest';
import { noAnswer, readAnswer, type Answer } from '../nodes/Status200Uploads/shared/answer';
import {
	DEFAULT_WAIT_SECONDS,
	MAX_SENDS,
	RETRY_TABLE,
	UNAVAILABLE_CODES,
	UNAVAILABLE_RESENDS,
	retryRuleFor,
	settle,
	type SettleOptions,
} from '../nodes/Status200Uploads/shared/retry';

function error(
	status: number,
	code: string,
	extra: Record<string, unknown> = {},
	headers: Record<string, string> = {},
): Answer {
	return readAnswer({
		statusCode: status,
		headers,
		body: { error: { code, message: `${code} message`, ...extra } },
	});
}

const ok = readAnswer({ statusCode: 200, body: { data: { tweet_id: '1' } } });

/** A settle run with scripted resends; records the waits and the resends. */
async function run(first: Answer, next: Answer[], options: Partial<SettleOptions> = {}) {
	const waits: number[] = [];
	let resends = 0;
	const settled = await settle(first, {
		send: async () => {
			resends++;
			const answer = next.shift();
			if (!answer) throw new Error('no scripted answer');
			return answer;
		},
		sleep: async (ms) => {
			waits.push(ms / 1000);
		},
		keySent: true,
		repeatable: false,
		waitWhenAsked: true,
		maxWaitSeconds: 120,
		...options,
	});
	return { settled, waits, resends };
}

describe('retryRuleFor', () => {
	it('reads the code first, then the status class, then not_json', () => {
		expect(retryRuleFor({ status: 409, code: 'media_processing', json: true })).toBe(
			'wait_and_resend',
		);
		expect(retryRuleFor({ status: 409, code: 'not_cancellable', json: true })).toBe('never');
		expect(retryRuleFor({ status: 500, code: 'something_new', json: true })).toBe(
			'resend_once_with_key',
		);
		expect(retryRuleFor({ status: 202, code: 'still_publishing', json: true })).toBe(
			'not_a_failure',
		);
		expect(retryRuleFor({ status: 200, json: true })).toBe('not_a_failure');
		expect(retryRuleFor({ status: 504, json: false })).toBe('resend_once_with_key');
		expect(retryRuleFor({ status: 0, json: false })).toBe('resend_once_with_key');
		expect(retryRuleFor({ status: 302, json: true })).toBe('never');
	});

	it('does not read a code inherited from Object', () => {
		expect(retryRuleFor({ status: 400, code: 'toString', json: true })).toBe('never');
	});
});

describe('settle: every 2xx is a success, never sent again', () => {
	for (const [status, body] of [
		[200, { data: { tweet_id: '1' } }],
		[200, { dry_run: true, outcome: 'refuse' }],
		[202, { code: 'scheduled', scheduled_post_id: 'x' }],
		[202, { code: 'queued_for_next_day' }],
		[202, { success: false, status: 'unknown', code: 'still_publishing', retry: false }],
		[202, { success: false, status: 'unknown', code: 'schedule_unconfirmed', retry: false }],
		[202, { data: { status: 'processing', job_id: 'j' } }],
	] as const) {
		it(`${status} ${JSON.stringify(body).slice(0, 50)}`, async () => {
			const { settled, resends } = await run(readAnswer({ statusCode: status, body }), []);
			expect(settled.ok).toBe(true);
			expect(resends).toBe(0);
		});
	}
});

describe('settle: wait_and_resend', () => {
	it('waits Retry-After, then sends the identical request again', async () => {
		const { settled, waits, resends } = await run(
			error(409, 'media_processing', { retry_after_seconds: 30 }, { 'retry-after': '30' }),
			[ok],
		);
		expect(settled.ok).toBe(true);
		expect(waits).toEqual([30]);
		expect(resends).toBe(1);
	});

	it('uses error.retry_after_seconds when there is no header, else 5 seconds', async () => {
		expect(
			(await run(error(429, 'rate_limited', { retry_after_seconds: 17 }), [ok])).waits,
		).toEqual([17]);
		expect((await run(error(409, 'idempotency_in_progress'), [ok])).waits).toEqual([
			DEFAULT_WAIT_SECONDS,
		]);
	});

	it('stops when Wait When Asked is off, saying how long the API asked to wait', async () => {
		const { settled, resends } = await run(
			error(429, 'rate_limited', { retry_after_seconds: 12 }),
			[ok],
			{
				waitWhenAsked: false,
			},
		);
		expect(settled).toMatchObject({ ok: false, reason: 'wait_off', askedWaitSeconds: 12 });
		expect(resends).toBe(0);
	});

	it('never waits past Max Wait in all', async () => {
		const busy = () =>
			error(409, 'media_processing', { retry_after_seconds: 30 }, { 'retry-after': '30' });
		const { settled, waits, resends } = await run(busy(), [busy(), busy(), busy(), busy()], {
			maxWaitSeconds: 100,
		});
		expect(waits).toEqual([30, 30, 30]);
		expect(resends).toBe(3);
		expect(settled).toMatchObject({
			ok: false,
			reason: 'max_wait',
			waitedSeconds: 90,
			askedWaitSeconds: 30,
		});
	});

	it('a wait longer than Max Wait (a daily limit) is not waited at all', async () => {
		const { settled, resends } = await run(
			error(429, 'rate_limited', { retry_after_seconds: 86000 }),
			[],
			{
				maxWaitSeconds: 600,
			},
		);
		expect(settled.reason).toBe('max_wait');
		expect(resends).toBe(0);
	});

	it(`sends a "nothing was sent" code again at most ${UNAVAILABLE_RESENDS} times`, async () => {
		for (const code of UNAVAILABLE_CODES) {
			const down = () => error(503, code, { retry_after_seconds: 5 }, { 'retry-after': '5' });
			const { settled, resends } = await run(down(), [down(), down(), down()]);
			expect(resends, code).toBe(UNAVAILABLE_RESENDS);
			expect(settled.reason, code).toBe('tries_used');
		}
	});

	it(`never sends more than ${MAX_SENDS} requests for one item`, async () => {
		const busy = () =>
			error(409, 'idempotency_in_progress', { retry_after_seconds: 1 }, { 'retry-after': '1' });
		const next = Array.from({ length: 50 }, busy);
		const { settled, resends } = await run(busy(), next, { maxWaitSeconds: 600 });
		expect(resends).toBe(MAX_SENDS - 1);
		expect(settled).toMatchObject({ ok: false, reason: 'tries_used', sends: MAX_SENDS });
	});
});

describe('settle: resend_once_with_key', () => {
	it('with a key: one more try, after Retry-After or 5 seconds', async () => {
		const page = readAnswer({ statusCode: 504, body: '<html>Gateway Timeout</html>' });
		const replayed = readAnswer({
			statusCode: 200,
			headers: { 'idempotent-replayed': 'true' },
			body: { data: { tweet_id: '1' } },
		});
		const { settled, waits, resends } = await run(page, [replayed]);
		expect(settled.ok).toBe(true);
		expect(settled.answer.replayed).toBe(true);
		expect(waits).toEqual([5]);
		expect(resends).toBe(1);
	});

	it('with a key: only once', async () => {
		const { settled, resends } = await run(error(500, 'server_error'), [
			error(500, 'server_error'),
			ok,
		]);
		expect(resends).toBe(1);
		expect(settled).toMatchObject({ ok: false, reason: 'once_used' });
	});

	it('without a key: not sent again (a POST whose outcome is not known)', async () => {
		for (const first of [
			error(500, 'platform_error'),
			noAnswer('socket hang up'),
			readAnswer({ statusCode: 502, body: 'Bad Gateway' }),
		]) {
			const { settled, resends } = await run(first, [ok], { keySent: false });
			expect(settled).toMatchObject({ ok: false, reason: 'no_key' });
			expect(resends).toBe(0);
		}
	});

	it('a read, a cancel or a dry run is sent again once without a key', async () => {
		const { settled, resends } = await run(error(500, 'server_error'), [ok], {
			keySent: false,
			repeatable: true,
		});
		expect(settled.ok).toBe(true);
		expect(resends).toBe(1);
	});

	it('is not bound by Wait When Asked (it is one short pause, not a wait the API asked for)', async () => {
		const { settled } = await run(noAnswer('ETIMEDOUT'), [ok], {
			waitWhenAsked: false,
			maxWaitSeconds: 0,
		});
		expect(settled.ok).toBe(true);
	});
});

describe('settle: never', () => {
	it('stops at once on every code the table marks never, and on any other 4xx', async () => {
		const codes = Object.entries(RETRY_TABLE.by_code)
			.filter(([, rule]) => rule === 'never')
			.map(([code]) => code);
		for (const code of [
			...codes,
			'bad_request',
			'account_not_found',
			'not_cancellable',
			'a_new_code',
		]) {
			const { settled, resends } = await run(error(422, code), [ok]);
			expect(settled, code).toMatchObject({ ok: false, reason: 'refused' });
			expect(resends, code).toBe(0);
		}
	});

	it('a code that means "accepted" on a status that is not 2xx contradicts itself: stop', async () => {
		const { settled, resends } = await run(error(400, 'scheduled'), [ok]);
		expect(settled.ok).toBe(false);
		expect(resends).toBe(0);
	});
});
