import { describe, expect, it } from 'vitest';
import {
	isSuccess,
	noAnswer,
	normalizeHeaders,
	readAnswer,
} from '../nodes/Status200Uploads/shared/answer';

describe('readAnswer', () => {
	it('reads the /api/v2 error shape: error.code, error.message, error.retry_after_seconds', () => {
		const a = readAnswer({
			statusCode: 429,
			headers: { 'Retry-After': '20', 'Content-Type': 'application/json' },
			body: {
				error: { code: 'rate_limited', message: 'Wait 20 seconds', retry_after_seconds: 20 },
			},
		});
		expect(a).toMatchObject({
			status: 429,
			json: true,
			code: 'rate_limited',
			message: 'Wait 20 seconds',
			retryAfterHeader: 20,
			retryAfterSeconds: 20,
			replayed: false,
		});
		expect(isSuccess(a)).toBe(false);
	});

	it('reads the media shape: the sentence in error, code and retry_after_seconds next to it', () => {
		const a = readAnswer({
			statusCode: 429,
			body: {
				error: 'Rate limited. Please wait 14 seconds.',
				code: 'rate_limited',
				retry_after_seconds: 14,
			},
		});
		expect(a).toMatchObject({
			code: 'rate_limited',
			message: 'Rate limited. Please wait 14 seconds.',
			retryAfterSeconds: 14,
		});
		expect(readAnswer({ statusCode: 400, body: { error: 'URL is required' } })).toMatchObject({
			code: undefined,
			message: 'URL is required',
		});
	});

	it('reads the media 429 whose error is an object (import_budget_exhausted)', () => {
		const a = readAnswer({
			statusCode: 429,
			body: {
				error: {
					code: 'import_budget_exhausted',
					message: 'Budget used',
					retry_after_seconds: 3600,
				},
			},
		});
		expect(a).toMatchObject({
			code: 'import_budget_exhausted',
			message: 'Budget used',
			retryAfterSeconds: 3600,
		});
	});

	it('reads a 202 by its code and message', () => {
		const a = readAnswer({
			statusCode: 202,
			body: { code: 'still_publishing', message: 'Do not send it again', retry: false },
		});
		expect(a).toMatchObject({ code: 'still_publishing', message: 'Do not send it again' });
		expect(isSuccess(a)).toBe(true);
	});

	it('marks Idempotent-Replayed answers', () => {
		expect(
			readAnswer({ statusCode: 200, headers: { 'Idempotent-Replayed': 'true' }, body: {} })
				.replayed,
		).toBe(true);
		expect(
			readAnswer({ statusCode: 200, headers: { 'idempotent-replayed': 'TRUE' }, body: {} })
				.replayed,
		).toBe(true);
	});

	it('reads a JSON body that came as text or bytes', () => {
		expect(
			readAnswer({
				statusCode: 409,
				body: '{"error":{"code":"idempotency_in_progress","message":"m"}}',
			}),
		).toMatchObject({
			json: true,
			code: 'idempotency_in_progress',
		});
		const bytes = new TextEncoder().encode('{"data":{"id":"1"}}');
		expect(readAnswer({ statusCode: 200, body: bytes })).toMatchObject({
			json: true,
			body: { data: { id: '1' } },
		});
	});

	it("keeps a gateway's page as text, not JSON", () => {
		const a = readAnswer({ statusCode: 504, body: '<html><body>Gateway Timeout</body></html>' });
		expect(a).toMatchObject({ status: 504, json: false, body: null });
		expect(a.text).toContain('Gateway Timeout');
		expect(readAnswer({ statusCode: 502, body: '{ not json' }).json).toBe(false);
		expect(readAnswer({ statusCode: 200, body: '' }).json).toBe(false);
	});

	it('ignores a Retry-After that is not a number of seconds', () => {
		expect(
			readAnswer({
				statusCode: 429,
				headers: { 'retry-after': 'Wed, 21 Oct 2026 07:28:00 GMT' },
				body: {},
			}).retryAfterHeader,
		).toBeUndefined();
	});

	it('noAnswer is status 0 and not JSON', () => {
		expect(noAnswer('socket hang up')).toMatchObject({
			status: 0,
			json: false,
			text: 'socket hang up',
		});
	});
});

describe('normalizeHeaders', () => {
	it('lower-cases names and joins lists', () => {
		expect(
			normalizeHeaders({ 'Retry-After': 5, 'Set-Cookie': ['a', 'b'], Skip: undefined }),
		).toEqual({
			'retry-after': '5',
			'set-cookie': 'a, b',
		});
		expect(normalizeHeaders(null)).toEqual({});
	});
});
