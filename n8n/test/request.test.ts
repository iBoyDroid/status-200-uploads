import { describe, expect, it } from 'vitest';
import { KEY_PATTERN } from '../nodes/Status200Uploads/shared/idempotency';
import { InvalidInput } from '../nodes/Status200Uploads/shared/input';
import {
	buildRequest,
	idFrom,
	splitList,
	type ParamReader,
	type RequestEnv,
} from '../nodes/Status200Uploads/shared/request';
import { check } from './support/spec';

const env: RequestEnv = {
	workflowId: 'wf1',
	executionId: '99',
	nodeId: 'node-1',
	itemIndex: 0,
	timezone: 'Europe/Berlin',
};

/** Parameters as getNodeParameter hands them over (resource locators already extracted). */
function reader(params: Record<string, unknown>): ParamReader {
	return {
		get(name, fallback) {
			let at: unknown = params;
			for (const part of name.split('.')) at = (at as Record<string, unknown> | undefined)?.[part];
			return at === undefined ? fallback : at;
		},
	};
}

const create = (extra: Record<string, unknown> = {}) =>
	reader({
		resource: 'post',
		operation: 'create',
		account: '@shop',
		platform: 'linkedin',
		text: 'Hello',
		...extra,
	});

describe('Post: Create', () => {
	it('builds {post} with an automatic Idempotency-Key, and the body fits PostRequest', () => {
		const req = buildRequest(create(), env);
		expect(req).toMatchObject({ method: 'POST', url: '/posts', keySent: true, repeatable: false });
		expect(req.body).toEqual({
			post: { accountId: '@shop', platform: 'linkedin', content: { text: 'Hello' } },
		});
		expect(req.headers['Idempotency-Key']).toMatch(/^n8n-[0-9a-f]{64}$/);
		expect(check('/components/schemas/PostRequest', req.body)).toBe('');
	});

	it('the same parameters give the same key; another item gives another', () => {
		const a = buildRequest(create(), env).headers['Idempotency-Key'];
		expect(buildRequest(create(), env).headers['Idempotency-Key']).toBe(a);
		expect(buildRequest(create(), { ...env, itemIndex: 1 }).headers['Idempotency-Key']).not.toBe(a);
	});

	it('media by URL (one per line) or by file ID (lines or commas)', () => {
		const urls = buildRequest(
			create({ media: 'urls', mediaUrls: 'https://a.example/1.jpg\n https://a.example/2,x.jpg ' }),
			env,
		);
		expect((urls.body as { post: { content: unknown } }).post.content).toEqual({
			text: 'Hello',
			mediaUrls: ['https://a.example/1.jpg', 'https://a.example/2,x.jpg'],
		});
		const ids = buildRequest(
			create({
				media: 'fileIds',
				fileIds: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890, b1b2c3d4-e5f6-7890-abcd-ef1234567890',
			}),
			env,
		);
		expect(
			(ids.body as { post: { content: { mediaID: string[] } } }).post.content.mediaID,
		).toHaveLength(2);
		const fromExpression = buildRequest(
			create({ media: 'urls', mediaUrls: ['https://a.example/1.mp4'] }),
			env,
		);
		expect(
			(fromExpression.body as { post: { content: { mediaUrls: string[] } } }).post.content
				.mediaUrls,
		).toEqual(['https://a.example/1.mp4']);
		expect(check('/components/schemas/PostRequest', urls.body)).toBe('');
		expect(() => buildRequest(create({ media: 'urls', mediaUrls: '  ' }), env)).toThrow(
			InvalidInput,
		);
	});

	it('At a Set Time: scheduledFor in the workflow time zone', () => {
		const req = buildRequest(create({ when: 'later', scheduledFor: '2026-10-01T09:00:00' }), env);
		expect((req.body as { post: { scheduledFor: string } }).post.scheduledFor).toBe(
			'2026-10-01T07:00:00.000Z',
		);
		expect(check('/components/schemas/PostRequest', req.body)).toBe('');
	});

	it('the per-network fields and options go into post.<platform>, lists split on commas', () => {
		const tiktok = buildRequest(
			create({
				platform: 'tiktok',
				tiktokPrivacyLevel: 'SELF_ONLY',
				tiktokOptions: { disabledDuet: true, title: ' Hi ' },
			}),
			env,
		);
		expect((tiktok.body as { post: Record<string, unknown> }).post.tiktok).toEqual({
			privacyLevel: 'SELF_ONLY',
			disabledDuet: true,
			title: 'Hi',
		});
		const youtube = buildRequest(
			create({
				platform: 'youtube',
				youtubePrivacyStatus: 'unlisted',
				youtubeOptions: { tags: 'a, b ,,c', madeForKids: false },
			}),
			env,
		);
		expect((youtube.body as { post: Record<string, unknown> }).post.youtube).toEqual({
			privacyStatus: 'unlisted',
			tags: ['a', 'b', 'c'],
			madeForKids: false,
		});
		const skool = buildRequest(
			create({
				platform: 'skool',
				skoolGroup: 'g1',
				skoolTitle: 'T',
				skoolOptions: { label: 'l1' },
			}),
			env,
		);
		expect((skool.body as { post: Record<string, unknown> }).post.skool).toEqual({
			group: 'g1',
			title: 'T',
			label: 'l1',
		});
		const pinterest = buildRequest(
			create({ platform: 'pinterest', pinterestBoardId: '900123' }),
			env,
		);
		expect((pinterest.body as { post: Record<string, unknown> }).post.pinterest).toEqual({
			boardId: '900123',
		});
		for (const req of [tiktok, youtube, skool, pinterest])
			expect(check('/components/schemas/PostRequest', req.body)).toBe('');
	});

	it('another network’s fields are not sent (only post.platform’s block is read)', () => {
		const req = buildRequest(
			create({ platform: 'x', tiktokPrivacyLevel: 'SELF_ONLY', youtubeOptions: { title: 'x' } }),
			env,
		);
		expect(Object.keys((req.body as { post: object }).post)).toEqual([
			'accountId',
			'platform',
			'content',
		]);
	});

	it('Additional Post Fields are merged in last (text or an object)', () => {
		const req = buildRequest(
			create({
				platform: 'tiktok',
				tiktokPrivacyLevel: 'PUBLIC_TO_EVERYONE',
				options: {
					additionalPostFields:
						'{"tiktok": {"isAiGenerated": true}, "content": {"text": "Override"}}',
				},
			}),
			env,
		);
		expect((req.body as { post: Record<string, unknown> }).post).toMatchObject({
			tiktok: { privacyLevel: 'PUBLIC_TO_EVERYONE', isAiGenerated: true },
			content: { text: 'Override' },
		});
		expect(() => buildRequest(create({ options: { additionalPostFields: '{nope' } }), env)).toThrow(
			/not valid JSON/,
		);
		expect(() => buildRequest(create({ options: { additionalPostFields: '[1]' } }), env)).toThrow(
			/not a JSON object/,
		);
		expect(
			buildRequest(
				create({ options: { additionalPostFields: { x: { whoCanReply: 'verified' } } } }),
				env,
			).body,
		).toMatchObject({
			post: { x: { whoCanReply: 'verified' } },
		});
	});

	it('Check Only: dryRun true, no key, safe to send again', () => {
		const req = buildRequest(create({ options: { dryRun: true } }), env);
		expect(req.body).toMatchObject({ dryRun: true });
		expect(req.headers).toEqual({});
		expect(req).toMatchObject({ keySent: false, repeatable: true });
		expect(check('/components/schemas/PostRequest', req.body)).toBe('');
	});

	it('Idempotency Key: custom (checked) or off', () => {
		const custom = buildRequest(
			create({
				options: { idempotencyKeyMode: 'custom', customIdempotencyKey: ' guid-1-linkedin ' },
			}),
			env,
		);
		expect(custom.headers['Idempotency-Key']).toBe('guid-1-linkedin');
		expect(KEY_PATTERN.test(custom.headers['Idempotency-Key'])).toBe(true);
		expect(() =>
			buildRequest(
				create({ options: { idempotencyKeyMode: 'custom', customIdempotencyKey: '' } }),
				env,
			),
		).toThrow(/empty/);
		const off = buildRequest(create({ options: { idempotencyKeyMode: 'off' } }), env);
		expect(off).toMatchObject({ headers: {}, keySent: false, repeatable: false });
	});

	it('refuses what cannot be sent, saying which parameter', () => {
		expect(() => buildRequest(create({ account: '' }), env)).toThrow(/Account is empty/);
		expect(() => buildRequest(create({ platform: 'myspace' }), env)).toThrow(/not known/);
		expect(() => buildRequest(create({ when: 'later', scheduledFor: '' }), env)).toThrow(
			/Scheduled For is empty/,
		);
	});
});

describe('the other operations', () => {
	const id = 'c3d4e5f6-a7b8-9012-cdef-123456789012';

	it('Post: Get and Cancel take an ID or a pasted status_url', () => {
		expect(
			buildRequest(reader({ resource: 'post', operation: 'get', post: id }), env),
		).toMatchObject({
			method: 'GET',
			url: `/posts/${id}`,
			repeatable: true,
		});
		expect(
			buildRequest(
				reader({
					resource: 'post',
					operation: 'cancel',
					scheduledPost: `https://status200uploads.com/api/v2/posts/${id.toUpperCase()}`,
				}),
				env,
			),
		).toMatchObject({ method: 'DELETE', url: `/posts/${id}`, repeatable: true });
		expect(
			buildRequest(reader({ resource: 'post', operation: 'cancel', scheduledPost: id }), env).body,
		).toBeUndefined();
		expect(() =>
			buildRequest(reader({ resource: 'post', operation: 'get', post: 'abc' }), env),
		).toThrow(/not an ID/);
	});

	it('Post: Get Many: limit, filters, 100 a page when returning all', () => {
		const req = buildRequest(
			reader({
				resource: 'post',
				operation: 'getAll',
				limit: 7,
				filters: { status: ['failed', 'timeout'], platform: 'x', kind: 'post', profileId: id },
			}),
			env,
		);
		expect(req.qs).toEqual({
			limit: 7,
			status: 'failed,timeout',
			platform: 'x',
			kind: 'post',
			profile_id: id,
		});
		expect(
			buildRequest(
				reader({ resource: 'post', operation: 'getAll', returnAll: true, limit: 7 }),
				env,
			).qs,
		).toEqual({ limit: 100 });
		expect(
			buildRequest(reader({ resource: 'post', operation: 'getAll', limit: 500 }), env).qs,
		).toEqual({ limit: 100 });
	});

	it('Account: Get Many and Get Posting Options', () => {
		expect(buildRequest(reader({ resource: 'account', operation: 'getAll' }), env)).toMatchObject({
			method: 'GET',
			url: '/accounts',
			qs: {},
		});
		expect(
			buildRequest(
				reader({
					resource: 'account',
					operation: 'getPostingOptions',
					profile: id,
					platforms: ['tiktok', 'skool'],
					skoolGroupSlug: 'grp',
				}),
				env,
			),
		).toMatchObject({
			url: `/accounts/${id}/options`,
			qs: { platforms: 'tiktok,skool', skool_group_slug: 'grp' },
		});
	});

	it('Media: Import From URL (with its own key) and Get', () => {
		const imp = buildRequest(
			reader({ resource: 'media', operation: 'importFromUrl', url: ' https://a.example/v.mp4 ' }),
			env,
		);
		expect(imp).toMatchObject({
			method: 'POST',
			url: '/media',
			body: { url: 'https://a.example/v.mp4' },
			keySent: true,
		});
		expect(check('/components/schemas/MediaImportRequest', imp.body)).toBe('');
		expect(
			buildRequest(reader({ resource: 'media', operation: 'get', fileId: id }), env),
		).toMatchObject({
			url: '/media',
			qs: { file_id: id },
		});
		expect(() =>
			buildRequest(reader({ resource: 'media', operation: 'importFromUrl', url: '' }), env),
		).toThrow(/URL is empty/);
	});

	it('an unknown operation is refused', () => {
		expect(() => buildRequest(reader({ resource: 'post', operation: 'delete' }), env)).toThrow(
			/not known/,
		);
	});
});

describe('helpers', () => {
	it('splitList and idFrom', () => {
		expect(splitList(' a ,b,, c ', /,/)).toEqual(['a', 'b', 'c']);
		expect(splitList([' a', 2, ''], /,/)).toEqual(['a', '2']);
		expect(
			idFrom(
				'https://status200uploads.com/api/v2/posts/c3d4e5f6-a7b8-9012-cdef-123456789012?x=1',
				'Post',
				'',
			),
		).toBe('c3d4e5f6-a7b8-9012-cdef-123456789012');
		expect(() => idFrom('', 'Post', 'hint')).toThrow(/Post is empty/);
	});
});
