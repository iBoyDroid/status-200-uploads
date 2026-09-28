import { describe, expect, it } from 'vitest';
import {
	KEY_MAX_LENGTH,
	KEY_PATTERN,
	automaticKey,
	canonicalJson,
	checkCustomKey,
} from '../nodes/Status200Uploads/shared/idempotency';

const inputs = { workflowId: 'wf1', executionId: '42', nodeId: 'node-a', itemIndex: 0 };
const body = { post: { accountId: '@shop', platform: 'x', content: { text: 'Hello' } } };

describe('canonicalJson', () => {
	it('sorts keys at every level and keeps list order', () => {
		expect(canonicalJson({ b: 1, a: { d: [3, 1], c: null } })).toBe(
			'{"a":{"c":null,"d":[3,1]},"b":1}',
		);
		expect(canonicalJson({ a: undefined, b: 'x' })).toBe('{"b":"x"}');
	});
});

describe('automaticKey', () => {
	it('is n8n- and 64 hex characters, a valid Idempotency-Key', () => {
		const key = automaticKey(inputs, body);
		expect(key).toMatch(/^n8n-[0-9a-f]{64}$/);
		expect(key.length).toBeLessThanOrEqual(KEY_MAX_LENGTH);
		expect(KEY_PATTERN.test(key)).toBe(true);
	});

	it('is the same for the same run, node, item and body, whatever the key order (Retry On Fail)', () => {
		const reordered = { post: { content: { text: 'Hello' }, platform: 'x', accountId: '@shop' } };
		expect(automaticKey(inputs, reordered)).toBe(automaticKey(inputs, body));
	});

	it('differs for another item, execution, node, workflow or body', () => {
		const key = automaticKey(inputs, body);
		expect(automaticKey({ ...inputs, itemIndex: 1 }, body)).not.toBe(key);
		expect(automaticKey({ ...inputs, executionId: '43' }, body)).not.toBe(key);
		expect(automaticKey({ ...inputs, nodeId: 'node-b' }, body)).not.toBe(key);
		expect(automaticKey({ ...inputs, workflowId: 'wf2' }, body)).not.toBe(key);
		expect(automaticKey(inputs, { post: { ...body.post, platform: 'linkedin' } })).not.toBe(key);
	});
});

describe('checkCustomKey', () => {
	it('accepts 1 to 255 printable ASCII characters, trimmed', () => {
		expect(checkCustomKey('  rss-123-tiktok  ')).toEqual({ key: 'rss-123-tiktok' });
		expect(checkCustomKey(12345)).toEqual({ key: '12345' });
		expect(checkCustomKey('x'.repeat(255))).toEqual({ key: 'x'.repeat(255) });
	});

	it('refuses an empty, too long or non-ASCII key', () => {
		expect(checkCustomKey('')).toHaveProperty('reason');
		expect(checkCustomKey('   ')).toHaveProperty('reason');
		expect(checkCustomKey(undefined)).toHaveProperty('reason');
		expect(checkCustomKey('x'.repeat(256))).toHaveProperty('reason');
		expect(checkCustomKey('café-post')).toHaveProperty('reason');
		expect(checkCustomKey('tab\there')).toHaveProperty('reason');
	});
});
