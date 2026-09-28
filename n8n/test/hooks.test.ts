// Items through the node as n8n runs them (preSend, the request, postReceive), with scripted answers.
// n8n-workflow's sleep is replaced by a recorder, so waits cost no time and can be checked.

import { NodeApiError, NodeOperationError } from 'n8n-workflow';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { API_BASE_URL, USER_AGENT } from '../nodes/Status200Uploads/shared/constants';
import { FakeHttp, itemContext, json, locator, runItem } from './support/fake';
import { responseExamples } from './support/spec';

const slept = vi.hoisted(() => ({ ms: [] as number[] }));
vi.mock('n8n-workflow', async (importOriginal) => {
	const actual = await importOriginal<Record<string, unknown>>();
	return {
		...actual,
		sleep: async (ms: number) => {
			slept.ms.push(ms);
		},
	};
});

const totalSeconds = () => slept.ms.reduce((a, b) => a + b, 0) / 1000;

beforeEach(() => {
	slept.ms.length = 0;
});

const ACCOUNT = locator('d4e5f6a7-b8c9-0123-def0-234567890123');
const POST_ID = 'b2c3d4e5-f6a7-8901-bcde-f12345678901';
const published = responseExamples('Published');
const accepted = responseExamples('Accepted');

function createPost(extra: Record<string, unknown> = {}) {
	return {
		resource: 'post',
		operation: 'create',
		account: ACCOUNT,
		platform: 'x',
		text: 'Hello from n8n',
		...extra,
	};
}

function refusal(
	status: number,
	code: string,
	extra: Record<string, unknown> = {},
	headers: Record<string, string> = {},
) {
	return json(status, { error: { code, message: `The API says ${code}`, ...extra } }, headers);
}

async function failure(promise: Promise<unknown>): Promise<NodeApiError> {
	const error = await promise.then(
		() => undefined,
		(e: unknown) => e,
	);
	expect(error).toBeInstanceOf(NodeApiError);
	return error as NodeApiError;
}

describe('Post: Create', () => {
	it('sends one request to /api/v2/posts with the key, the User-Agent and the body; outputs the answer', async () => {
		const http = new FakeHttp().answer(json(200, published.x));
		const out = await runItem(itemContext(createPost(), http), http);
		expect(http.sent).toHaveLength(1);
		const [sent] = http.sent;
		expect(sent).toMatchObject({
			baseURL: API_BASE_URL,
			url: '/posts',
			method: 'POST',
			json: true,
			returnFullResponse: true,
			ignoreHttpStatusErrors: true,
			body: {
				post: {
					accountId: 'd4e5f6a7-b8c9-0123-def0-234567890123',
					platform: 'x',
					content: { text: 'Hello from n8n' },
				},
			},
		});
		expect((sent.headers as Record<string, string>)['User-Agent']).toBe(USER_AGENT);
		expect((sent.headers as Record<string, string>)['Idempotency-Key']).toMatch(
			/^n8n-[0-9a-f]{64}$/,
		);
		expect(http.credentialTypes).toEqual(['status200UploadsApi']);
		expect(out).toEqual([{ json: published.x, pairedItem: { item: 0 } }]);
	});

	it('an @handle from the locator is sent as the accountId', async () => {
		const http = new FakeHttp().answer(json(200, published.linkedin));
		await runItem(
			itemContext(
				createPost({ account: locator('@myshop', 'handle'), platform: 'linkedin' }),
				http,
			),
			http,
		);
		expect(http.sent[0].body).toMatchObject({ post: { accountId: '@myshop' } });
	});

	for (const name of Object.keys(accepted)) {
		it(`202 ${name} is a success output, never sent again`, async () => {
			const http = new FakeHttp().answer(json(202, accepted[name]));
			const out = await runItem(itemContext(createPost(), http), http);
			expect(http.sent).toHaveLength(1);
			expect(out[0].json).toEqual(accepted[name]);
		});
	}

	it('409 media_processing: waits Retry-After, sends the identical request, outputs the post', async () => {
		const http = new FakeHttp().answer(
			refusal(
				409,
				'media_processing',
				{ file_id: 'f', progress: 40, retry_after_seconds: 30 },
				{ 'Retry-After': '30' },
			),
			json(200, published.tiktok),
		);
		const out = await runItem(
			itemContext(
				createPost({
					platform: 'tiktok',
					tiktokPrivacyLevel: 'SELF_ONLY',
					media: 'fileIds',
					fileIds: POST_ID,
				}),
				http,
			),
			http,
		);
		expect(http.sent).toHaveLength(2);
		expect(http.sent[1]).toEqual(http.sent[0]);
		expect(totalSeconds()).toBe(30);
		expect(out[0].json).toEqual(published.tiktok);
	});

	it('a replayed answer (the first answer to this key) is marked replayed', async () => {
		const http = new FakeHttp().answer(
			{ status: 504, body: '<html>Gateway Timeout</html>' },
			json(200, published.linkedin, { 'Idempotent-Replayed': 'true' }),
		);
		const out = await runItem(itemContext(createPost({ platform: 'linkedin' }), http), http);
		expect(http.sent).toHaveLength(2);
		expect(http.sent[1].headers).toEqual(http.sent[0].headers);
		expect(out[0].json).toEqual({ ...published.linkedin, replayed: true });
	});

	it('$now in Text: the resend after a page that is not JSON is the identical request', async () => {
		let reads = 0;
		const http = new FakeHttp().answer(
			{ status: 504, body: '<html>Gateway Timeout</html>' },
			json(200, published.x, { 'Idempotent-Replayed': 'true' }),
		);
		await runItem(
			itemContext(createPost(), http, { volatile: { text: () => `Update at ${++reads}` } }),
			http,
		);
		expect(http.sent).toHaveLength(2);
		expect(http.sent[0].body).toMatchObject({ post: { content: { text: 'Update at 1' } } });
		expect(http.sent[1]).toEqual(http.sent[0]);
	});

	it('$now in Scheduled For: the resend after 409 idempotency_in_progress is the identical request', async () => {
		let reads = 0;
		const later = () => new Date(Date.UTC(2026, 9, 1, 9, 0, 0, ++reads)).toISOString();
		const http = new FakeHttp().answer(
			refusal(409, 'idempotency_in_progress', { retry_after_seconds: 5 }, { 'Retry-After': '5' }),
			json(202, accepted[Object.keys(accepted)[0]]),
		);
		await runItem(
			itemContext(createPost({ platform: 'linkedin', when: 'later' }), http, {
				volatile: { scheduledFor: later },
			}),
			http,
		);
		expect(http.sent).toHaveLength(2);
		expect(http.sent[0].body).toMatchObject({
			post: { scheduledFor: '2026-10-01T09:00:00.001Z' },
		});
		expect(http.sent[1]).toEqual(http.sent[0]);
	});

	it('without a key, a page that is not JSON is not sent again: check History first', async () => {
		const http = new FakeHttp().answer({ status: 504, body: '<html>Gateway Timeout</html>' });
		const error = await failure(
			runItem(itemContext(createPost({ options: { idempotencyKeyMode: 'off' } }), http), http),
		);
		expect(http.sent).toHaveLength(1);
		expect(error.httpCode).toBe('504');
		expect(error.description).toMatch(/without an Idempotency-Key/);
		expect(error.description).toMatch(/History/);
	});

	it('a connection that breaks during a resend is an unknown outcome, sent once more only', async () => {
		const reset = Object.assign(new Error('socket hang up'), { code: 'ECONNRESET' });
		const wrapped = new NodeApiError(
			{ id: 'n', name: 'n', type: 't', typeVersion: 1, position: [0, 0], parameters: {} },
			reset as never,
		);
		const http = new FakeHttp().answer(refusal(500, 'server_error'), { throws: wrapped });
		const error = await failure(runItem(itemContext(createPost(), http), http));
		expect(http.sent).toHaveLength(2);
		expect(error.description).toMatch(/Sent once more with the same Idempotency-Key/);
		expect(error.description).toMatch(/\(no answer\)$/);
		expect(error.httpCode).toBeNull();
	});

	it('429 monthly_limit_reached stops at once with the facts and the fix', async () => {
		const http = new FakeHttp().answer(
			refusal(429, 'monthly_limit_reached', {
				upgrade_url: 'https://status200uploads.com/pricing',
				used: 60,
				limit: 60,
				window: 'month',
				resets_at: '2026-10-01T00:00:00.000Z',
				plan: 'free',
				trial_available: true,
				retry_after_seconds: 200000,
			}),
		);
		const error = await failure(runItem(itemContext(createPost(), http), http));
		expect(http.sent).toHaveLength(1);
		expect(error.message).toBe('The API says monthly_limit_reached [item 0]');
		expect(error.httpCode).toBe('429');
		expect(error.description).toContain('Comes back at 2026-10-01T00:00:00.000Z.');
		expect(error.description).toContain('Upgrade: https://status200uploads.com/pricing');
		expect(error.description).toContain('code monthly_limit_reached');
	});

	it('429 rate_limited within Max Wait: waits and sends again', async () => {
		const http = new FakeHttp().answer(
			refusal(429, 'rate_limited', { retry_after_seconds: 20 }, { 'Retry-After': '20' }),
			json(200, published.x),
		);
		await runItem(itemContext(createPost(), http), http);
		expect(http.sent).toHaveLength(2);
		expect(totalSeconds()).toBe(20);
	});

	it('Wait When Asked off: stops with the wait the API asked for', async () => {
		const http = new FakeHttp().answer(
			refusal(429, 'rate_limited', { retry_after_seconds: 20 }, { 'Retry-After': '20' }),
		);
		const error = await failure(
			runItem(itemContext(createPost({ options: { waitWhenAsked: false } }), http), http),
		);
		expect(http.sent).toHaveLength(1);
		expect(error.description).toMatch(/asked to wait 20 seconds/);
	});

	it('Max Wait caps the waits in all', async () => {
		const busy = () =>
			refusal(
				409,
				'media_processing',
				{ file_id: 'f', progress: 1, retry_after_seconds: 30 },
				{ 'Retry-After': '30' },
			);
		const http = new FakeHttp().answer(busy(), busy(), busy());
		const error = await failure(
			runItem(itemContext(createPost({ options: { maxWait: 45 } }), http), http),
		);
		expect(http.sent).toHaveLength(2);
		expect(totalSeconds()).toBe(30);
		expect(error.description).toMatch(/Max Wait \(45 seconds in all\)/);
	});

	it('422 idempotency_key_reused is never sent again', async () => {
		const http = new FakeHttp().answer(
			refusal(422, 'idempotency_key_reused', { first_used_at: '2026-09-28T10:00:00Z' }),
		);
		const error = await failure(runItem(itemContext(createPost(), http), http));
		expect(http.sent).toHaveLength(1);
		expect(error.description).toMatch(/no \$now/);
	});

	it('403 account_not_found names the profiles', async () => {
		const http = new FakeHttp().answer(
			refusal(403, 'account_not_found', { profiles: ['@a', '@b'] }),
		);
		const error = await failure(runItem(itemContext(createPost(), http), http));
		expect(error.description).toContain('Your profiles: @a, @b.');
	});

	it('a dry run sends no key, and its report is the output', async () => {
		const http = new FakeHttp().answer(json(200, published.dryRun));
		const out = await runItem(itemContext(createPost({ options: { dryRun: true } }), http), http);
		expect((http.sent[0].headers as Record<string, string>)['Idempotency-Key']).toBeUndefined();
		expect(http.sent[0].body).toMatchObject({ dryRun: true });
		expect(out[0].json).toEqual(published.dryRun);
	});

	it('a parameter that cannot be sent stops before any request', async () => {
		const http = new FakeHttp();
		const error = await runItem(
			itemContext(createPost({ when: 'later', scheduledFor: '' }), http),
			http,
		).then(
			() => undefined,
			(e: unknown) => e,
		);
		expect(error).toBeInstanceOf(NodeOperationError);
		expect((error as Error).message).toBe('Scheduled For is empty [item 0]');
		expect(http.sent).toHaveLength(0);
	});

	it('with no execution id, the key is still the same for the request and its resend', async () => {
		const http = new FakeHttp().answer(
			refusal(409, 'idempotency_in_progress', { retry_after_seconds: 5 }),
			json(200, published.x),
		);
		await runItem(itemContext(createPost(), http, { executionId: '' }), http);
		expect(http.sent).toHaveLength(2);
		expect(http.sent[1].headers).toEqual(http.sent[0].headers);
	});

	it('the item index is in the key, the message and pairedItem', async () => {
		const http = new FakeHttp().answer(json(200, published.x), json(200, published.x));
		const a = await runItem(itemContext(createPost(), http, { itemIndex: 0 }), http);
		const b = await runItem(itemContext(createPost(), http, { itemIndex: 3 }), http);
		expect(http.sent[0].headers).not.toEqual(http.sent[1].headers);
		expect(a[0].pairedItem).toEqual({ item: 0 });
		expect(b[0].pairedItem).toEqual({ item: 3 });
	});

	it('a cancelled execution stops the wait', async () => {
		const controller = new AbortController();
		controller.abort();
		const http = new FakeHttp().answer(
			refusal(429, 'rate_limited', { retry_after_seconds: 20 }),
			json(200, published.x),
		);
		const error = await runItem(
			itemContext(createPost(), http, { signal: controller.signal }),
			http,
		).then(
			() => undefined,
			(e: unknown) => e,
		);
		expect(error).toBeInstanceOf(NodeOperationError);
		expect(http.sent).toHaveLength(1);
	});
});

describe('Post: Get, Get Many, Cancel', () => {
	const post = {
		id: POST_ID,
		kind: 'post',
		profile_id: 'd4e5f6a7-b8c9-0123-def0-234567890123',
		platform: 'x',
		status: 'success',
		done: true,
		media_type: null,
		publish_id: '1841234567890123456',
		permalink: 'https://x.com/i/status/1841234567890123456',
		error_message: null,
		at: '2026-09-28T10:00:00.000Z',
		updated_at: '2026-09-28T10:00:01.000Z',
		scheduled_post_id: null,
		figures: null,
	};

	it('Get: a pasted status_url, simplified', async () => {
		const http = new FakeHttp().answer(json(200, { data: post }));
		const out = await runItem(
			itemContext(
				{
					resource: 'post',
					operation: 'get',
					post: locator(`https://status200uploads.com/api/v2/posts/${POST_ID}`, 'url'),
				},
				http,
			),
			http,
		);
		expect(http.sent[0]).toMatchObject({ method: 'GET', url: `/posts/${POST_ID}` });
		expect(http.sent[0].body).toBeUndefined();
		expect(out[0].json).toEqual({
			id: POST_ID,
			kind: 'post',
			platform: 'x',
			status: 'success',
			done: true,
			permalink: post.permalink,
			error_message: null,
			at: post.at,
			scheduled_post_id: null,
		});
	});

	it('Get: Simplify off gives the whole post', async () => {
		const http = new FakeHttp().answer(json(200, { data: post }));
		const out = await runItem(
			itemContext(
				{ resource: 'post', operation: 'get', post: locator(POST_ID, 'id'), simplify: false },
				http,
			),
			http,
		);
		expect(out[0].json).toEqual(post);
	});

	it('Get Many with Return All follows next_cursor, reading 100 a page', async () => {
		const page = (n: number, next: string | null) =>
			json(200, {
				data: [{ ...post, id: `${n}` }],
				next_cursor: next,
				next_url: next ? `${API_BASE_URL}/posts?cursor=${next}` : null,
			});
		const http = new FakeHttp().answer(page(1, 'c1'), page(2, 'c2'), page(3, null));
		const out = await runItem(
			itemContext(
				{
					resource: 'post',
					operation: 'getAll',
					returnAll: true,
					filters: { platform: 'x' },
					simplify: false,
				},
				http,
			),
			http,
		);
		expect(out.map((i) => i.json.id)).toEqual(['1', '2', '3']);
		expect(http.sent.map((s) => s.qs)).toEqual([
			{ limit: 100, platform: 'x' },
			{ limit: 100, platform: 'x', cursor: 'c1' },
			{ limit: 100, platform: 'x', cursor: 'c2' },
		]);
		expect(out.every((i) => (i.pairedItem as { item: number }).item === 0)).toBe(true);
	});

	it('Get Many: a read limit is waited for, then the page is read again', async () => {
		const http = new FakeHttp().answer(
			refusal(429, 'rate_limited', { retry_after_seconds: 12, limit: 60 }, { 'Retry-After': '12' }),
			json(200, { data: [post], next_cursor: null, next_url: null }),
		);
		const out = await runItem(
			itemContext({ resource: 'post', operation: 'getAll', limit: 5 }, http),
			http,
		);
		expect(out).toHaveLength(1);
		expect(totalSeconds()).toBe(12);
	});

	it('Cancel: DELETE, the answer’s data (twice is fine)', async () => {
		const data = {
			scheduled_post_id: POST_ID,
			status: 'cancelled',
			platforms: ['tiktok'],
			was_due_at: '2026-10-01T09:00:00+00:00',
			message: 'Already cancelled.',
			already_cancelled: true,
		};
		const http = new FakeHttp().answer(json(200, { data }));
		const out = await runItem(
			itemContext({ resource: 'post', operation: 'cancel', scheduledPost: locator(POST_ID) }, http),
			http,
		);
		expect(http.sent[0]).toMatchObject({ method: 'DELETE', url: `/posts/${POST_ID}` });
		expect(out[0].json).toEqual(data);
	});

	it('Cancel: 504 cancel_unconfirmed is sent again after its wait', async () => {
		const http = new FakeHttp().answer(
			refusal(504, 'cancel_unconfirmed', { retry_after_seconds: 5 }, { 'Retry-After': '5' }),
			json(200, {
				data: {
					scheduled_post_id: POST_ID,
					status: 'cancelled',
					platforms: [],
					was_due_at: 'x',
					message: 'm',
				},
			}),
		);
		await runItem(
			itemContext({ resource: 'post', operation: 'cancel', scheduledPost: locator(POST_ID) }, http),
			http,
		);
		expect(http.sent).toHaveLength(2);
	});

	it('Cancel: 409 not_cancellable says why', async () => {
		const http = new FakeHttp().answer(refusal(409, 'not_cancellable', { status: 'published' }));
		const error = await failure(
			runItem(
				itemContext(
					{ resource: 'post', operation: 'cancel', scheduledPost: locator(POST_ID) },
					http,
				),
				http,
			),
		);
		expect(error.description).toContain('Status: published.');
	});
});

describe('Account', () => {
	const accounts = Array.from({ length: 4 }, (_, i) => ({
		profile_id: `0000000${i}-b8c9-0123-def0-234567890123`,
		profile_name: `shop${i}`,
		handle: `@shop${i}`,
		created_at: null,
		networks: [],
	}));

	it('Get Many: one item per profile, up to Limit', async () => {
		const http = new FakeHttp().answer(json(200, { data: accounts }));
		const out = await runItem(
			itemContext({ resource: 'account', operation: 'getAll', limit: 2 }, http),
			http,
		);
		expect(out.map((i) => i.json.handle)).toEqual(['@shop0', '@shop1']);
	});

	it('Get Posting Options: the answer’s data', async () => {
		const data = {
			profile_id: accounts[0].profile_id,
			profile_name: 'shop0',
			networks: [],
			note: null,
			asked_at: '2026-09-28T10:00:00Z',
		};
		const http = new FakeHttp().answer(json(200, { data }));
		const out = await runItem(
			itemContext(
				{
					resource: 'account',
					operation: 'getPostingOptions',
					profile: locator(accounts[0].profile_id),
					platforms: ['tiktok'],
				},
				http,
			),
			http,
		);
		expect(http.sent[0]).toMatchObject({
			url: `/accounts/${accounts[0].profile_id}/options`,
			qs: { platforms: 'tiktok' },
		});
		expect(out[0].json).toEqual(data);
	});

	it('401 unauthorized: says to check the credential', async () => {
		const http = new FakeHttp().answer(refusal(401, 'unauthorized'));
		const error = await failure(
			runItem(itemContext({ resource: 'account', operation: 'getAll' }, http), http),
		);
		expect(error.httpCode).toBe('401');
		expect(error.description).toMatch(/API key in the credential/);
	});
});

describe('Media', () => {
	const FILE = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';

	it('Import From URL waits until the file is ready', async () => {
		const http = new FakeHttp().answer(
			json(202, {
				success: true,
				file_id: FILE,
				status: 'processing',
				message: 'Import continues',
				size: null,
				type: 'video/mp4',
			}),
			json(200, {
				success: false,
				file_id: FILE,
				status: 'processing',
				size: 1000,
				type: 'video/mp4',
				public_url: null,
				error: null,
				progress: 50,
			}),
			json(200, {
				success: true,
				file_id: FILE,
				status: 'ready',
				size: 1000,
				type: 'video/mp4',
				public_url: 'https://x/y.mp4',
				error: null,
			}),
		);
		const out = await runItem(
			itemContext(
				{ resource: 'media', operation: 'importFromUrl', url: 'https://a.example/v.mp4' },
				http,
			),
			http,
		);
		expect(http.sent[0]).toMatchObject({
			method: 'POST',
			url: '/media',
			body: { url: 'https://a.example/v.mp4' },
		});
		expect((http.sent[0].headers as Record<string, string>)['Idempotency-Key']).toMatch(/^n8n-/);
		expect(http.sent.slice(1).map((s) => [s.method, s.url, s.qs])).toEqual([
			['GET', '/media', { file_id: FILE }],
			['GET', '/media', { file_id: FILE }],
		]);
		expect(totalSeconds()).toBe(10);
		expect(out[0].json).toMatchObject({ file_id: FILE, status: 'ready' });
	});

	it('Max Wait covers the import and the wait until ready together', async () => {
		const processing = {
			success: false,
			file_id: FILE,
			status: 'processing',
			size: 1000,
			type: 'video/mp4',
			public_url: null,
			error: null,
			progress: 10,
		};
		const http = new FakeHttp().answer(
			json(
				429,
				{
					error: 'Rate limited. Please wait 20 seconds.',
					code: 'rate_limited',
					retry_after_seconds: 20,
				},
				{ 'Retry-After': '20' },
			),
			json(202, {
				success: true,
				file_id: FILE,
				status: 'processing',
				message: 'Import continues',
				size: null,
				type: 'video/mp4',
			}),
			...Array.from({ length: 10 }, () => json(200, processing)),
		);
		const out = await runItem(
			itemContext(
				{
					resource: 'media',
					operation: 'importFromUrl',
					url: 'https://a.example/v.mp4',
					options: { maxWait: 30 },
				},
				http,
			),
			http,
		);
		// 20 seconds for the rate limit, then two reads 5 seconds apart: 30 seconds in all.
		expect(totalSeconds()).toBe(30);
		expect(http.sent.filter((s) => s.method === 'GET')).toHaveLength(2);
		expect(out[0].json).toMatchObject({ file_id: FILE, status: 'processing' });
	});

	it('an import that failed stops with its reason', async () => {
		const http = new FakeHttp().answer(
			json(202, {
				success: true,
				file_id: FILE,
				status: 'processing',
				message: 'm',
				size: null,
				type: 'video/mp4',
			}),
			json(200, {
				success: false,
				file_id: FILE,
				status: 'failed',
				size: null,
				type: null,
				public_url: null,
				error: 'Source answered 404',
			}),
		);
		const error = await failure(
			runItem(
				itemContext(
					{ resource: 'media', operation: 'importFromUrl', url: 'https://a.example/v.mp4' },
					http,
				),
				http,
			),
		);
		expect(error.message).toBe(
			'The import of the file did not finish: Source answered 404 [item 0]',
		);
	});

	it('Wait Until Ready off: the import answer as it is', async () => {
		const started = {
			success: true,
			file_id: FILE,
			status: 'processing',
			message: 'm',
			size: null,
			type: 'video/mp4',
		};
		const http = new FakeHttp().answer(json(202, started));
		const out = await runItem(
			itemContext(
				{
					resource: 'media',
					operation: 'importFromUrl',
					url: 'https://a.example/v.mp4',
					options: { waitUntilReady: false },
				},
				http,
			),
			http,
		);
		expect(out[0].json).toEqual(started);
		expect(http.sent).toHaveLength(1);
	});

	it('the media 429 shape (sentence in error, retry_after_seconds beside it) is waited for', async () => {
		const http = new FakeHttp().answer(
			json(
				429,
				{
					error: 'Rate limited. Please wait 14 seconds.',
					code: 'rate_limited',
					retry_after_seconds: 14,
				},
				{ 'Retry-After': '14' },
			),
			json(200, { success: true, file_id: FILE, size: 10, type: 'image/jpeg', status: 'ready' }),
		);
		const out = await runItem(
			itemContext(
				{ resource: 'media', operation: 'importFromUrl', url: 'https://a.example/p.jpg' },
				http,
			),
			http,
		);
		expect(totalSeconds()).toBe(14);
		expect(http.sent[1]).toEqual(http.sent[0]);
		expect(out[0].json).toMatchObject({ status: 'ready' });
	});

	it('a media refusal without a code gets the media fix line', async () => {
		const http = new FakeHttp().answer(
			json(415, { error: 'URL does not point to an image or video' }),
		);
		const error = await failure(
			runItem(
				itemContext(
					{ resource: 'media', operation: 'importFromUrl', url: 'https://a.example/page' },
					http,
				),
				http,
			),
		);
		expect(error.message).toBe('URL does not point to an image or video [item 0]');
		expect(error.description).toMatch(/not a web page/);
	});

	it('Get: the status as it is', async () => {
		const status = {
			success: true,
			file_id: FILE,
			status: 'ready',
			size: 1,
			type: 'image/png',
			public_url: 'https://x/y.png',
			error: null,
		};
		const http = new FakeHttp().answer(json(200, status));
		const out = await runItem(
			itemContext({ resource: 'media', operation: 'get', fileId: FILE }, http),
			http,
		);
		expect(http.sent[0]).toMatchObject({ method: 'GET', url: '/media', qs: { file_id: FILE } });
		expect(out[0].json).toEqual(status);
	});
});
