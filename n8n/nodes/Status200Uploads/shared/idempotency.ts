import { createHash } from 'crypto';

/** components.parameters.IdempotencyKey of the OpenAPI file: 1 to 255 printable ASCII characters. */
export const KEY_MAX_LENGTH = 255;
export const KEY_PATTERN = /^[\x20-\x7E]+$/;

/** What makes one request of one item of one run unique. */
export interface KeyInputs {
	workflowId: string;
	executionId: string;
	nodeId: string;
	itemIndex: number;
}

/**
 * JSON with the keys of every object sorted, so that the same body always gives the same text (the
 * API compares bodies the same way).
 */
export function canonicalJson(value: unknown): string {
	if (value === null || typeof value !== 'object') {
		const text = JSON.stringify(value);
		return text === undefined ? 'null' : text;
	}
	if (Array.isArray(value)) return `[${value.map((v) => canonicalJson(v)).join(',')}]`;
	const entries = Object.keys(value as Record<string, unknown>)
		.filter((k) => (value as Record<string, unknown>)[k] !== undefined)
		.sort()
		.map((k) => `${JSON.stringify(k)}:${canonicalJson((value as Record<string, unknown>)[k])}`);
	return `{${entries.join(',')}}`;
}

/**
 * The automatic Idempotency-Key: "n8n-" and the SHA-256 of the workflow, the execution, the node, the
 * item and the body. n8n's Retry On Fail runs the node again in the same execution with the same items,
 * so it sends the same key and gets the first answer back instead of posting twice. Two different posts
 * in one execution (an AI agent's tool calls all use item 0) have different bodies, so different keys.
 * A new execution makes new keys: running the workflow again is a new post.
 */
export function automaticKey(inputs: KeyInputs, body: unknown): string {
	const text = [
		inputs.workflowId,
		inputs.executionId,
		inputs.nodeId,
		String(inputs.itemIndex),
		canonicalJson(body),
	].join('|');
	return `n8n-${createHash('sha256').update(text, 'utf8').digest('hex')}`;
}

/** A key typed in (or built by an expression), checked the way the API checks it. */
export function checkCustomKey(raw: unknown): { key: string } | { reason: string } {
	const key = typeof raw === 'number' ? String(raw) : typeof raw === 'string' ? raw.trim() : '';
	if (key === '') {
		return { reason: 'The Custom Idempotency Key is empty' };
	}
	if (key.length > KEY_MAX_LENGTH) {
		return {
			reason: `The Custom Idempotency Key is ${key.length} characters long (at most ${KEY_MAX_LENGTH})`,
		};
	}
	if (!KEY_PATTERN.test(key)) {
		return { reason: 'The Custom Idempotency Key has characters other than printable ASCII' };
	}
	return { key };
}
