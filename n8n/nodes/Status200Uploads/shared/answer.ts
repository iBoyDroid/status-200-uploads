import type { IDataObject } from 'n8n-workflow';

/**
 * One answer of the API, read the same way whatever its shape:
 *   - /api/v2 posts, accounts and reads: {"error": {"code", "message", ...}} (ErrorResponse);
 *   - /api/v2/media: {"error": "sentence", "code"?, "retry_after_seconds"?} (MediaError), where one
 *     429 (import_budget_exhausted) carries an object in `error` instead;
 *   - a 2xx: the body itself (a 202 names its case in `code`);
 *   - a gateway's page that is not JSON (Netlify's HTML 504), or no answer at all (status 0).
 */
export interface Answer {
	/** The HTTP status; 0 when no answer arrived (the connection broke or timed out). */
	status: number;
	/** Response headers, names in lower case. */
	headers: Record<string, string>;
	/** Whether the body is a JSON object. */
	json: boolean;
	/** The JSON body; null when it was not JSON. */
	body: IDataObject | null;
	/** The start of a body that was not JSON, or why no answer arrived. */
	text: string;
	/** error.code, the media shape's code, or a 2xx's code. */
	code?: string;
	/** error.message, the media shape's error sentence, or a 2xx's message. */
	message?: string;
	/** The Retry-After header, in seconds. */
	retryAfterHeader?: number;
	/** error.retry_after_seconds, or retry_after_seconds next to a media error. */
	retryAfterSeconds?: number;
	/** Idempotent-Replayed: true (the stored first answer to this Idempotency-Key). */
	replayed: boolean;
}

/** What n8n hands over with returnFullResponse. */
export interface FullResponse {
	statusCode?: number;
	headers?: unknown;
	body?: unknown;
}

const TEXT_KEPT = 500;

function isObject(value: unknown): value is IDataObject {
	return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function asString(value: unknown): string | undefined {
	return typeof value === 'string' ? value : undefined;
}

function asSeconds(value: unknown): number | undefined {
	const n = typeof value === 'string' && value.trim() !== '' ? Number(value) : value;
	return typeof n === 'number' && Number.isFinite(n) && n >= 0 ? Math.ceil(n) : undefined;
}

/** Header names in lower case, values as text (a list is joined). */
export function normalizeHeaders(headers: unknown): Record<string, string> {
	const out: Record<string, string> = {};
	if (!isObject(headers)) return out;
	for (const [name, value] of Object.entries(headers)) {
		if (value === undefined || value === null || typeof value === 'function') continue;
		out[name.toLowerCase()] = Array.isArray(value) ? value.map(String).join(', ') : String(value);
	}
	return out;
}

/** The body as text, when it came as text or bytes. */
function bodyText(body: unknown): string | undefined {
	if (typeof body === 'string') return body;
	if (body instanceof Uint8Array) return new TextDecoder().decode(body);
	return undefined;
}

/** The JSON object of a body, or null. */
function parseBody(body: unknown): IDataObject | null {
	if (isObject(body) && !(body instanceof Uint8Array)) return body;
	const text = bodyText(body)?.trim();
	if (!text || (text[0] !== '{' && text[0] !== '[')) return null;
	let parsed: unknown = null;
	try {
		parsed = JSON.parse(text);
	} catch {
		// Not JSON (a gateway's page that happens to start with a brace): read as text below.
		parsed = null;
	}
	return isObject(parsed) ? parsed : null;
}

/** Reads one full response into an Answer. */
export function readAnswer(response: FullResponse): Answer {
	const status = typeof response.statusCode === 'number' ? response.statusCode : 0;
	const headers = normalizeHeaders(response.headers);
	const body = parseBody(response.body);
	const answer: Answer = {
		status,
		headers,
		json: body !== null,
		body,
		text: body === null ? (bodyText(response.body) ?? '').slice(0, TEXT_KEPT) : '',
		replayed: (headers['idempotent-replayed'] ?? '').toLowerCase() === 'true',
		retryAfterHeader: asSeconds(headers['retry-after']),
	};
	if (body === null) return answer;

	const error = body.error;
	if (isObject(error)) {
		// ErrorResponse, and the media 429 import_budget_exhausted.
		answer.code = asString(error.code) ?? asString(body.code);
		answer.message = asString(error.message);
		answer.retryAfterSeconds =
			asSeconds(error.retry_after_seconds) ?? asSeconds(body.retry_after_seconds);
	} else if (typeof error === 'string') {
		// MediaError: the sentence in `error`, the code (when any) next to it.
		answer.code = asString(body.code);
		answer.message = error;
		answer.retryAfterSeconds = asSeconds(body.retry_after_seconds);
	} else {
		// A 2xx: a 202 names its case in `code` (scheduled, queued_for_next_day, still_publishing ...).
		answer.code = asString(body.code);
		answer.message = asString(body.message);
	}
	return answer;
}

/** The Answer of a request that got no answer: the connection broke, or it timed out. */
export function noAnswer(reason: string): Answer {
	return {
		status: 0,
		headers: {},
		json: false,
		body: null,
		text: reason.slice(0, TEXT_KEPT),
		replayed: false,
	};
}

/** Whether the answer is a success (2xx with a JSON body). */
export function isSuccess(answer: Answer): boolean {
	return answer.status >= 200 && answer.status < 300 && answer.json;
}
