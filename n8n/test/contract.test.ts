// The node against the OpenAPI file (../openapi/openapi.yaml, a copy of
// https://status200uploads.com/openapi.yaml): every request it sends exists on the main address, every
// field and choice it offers is one the file names, its retry table is the file's, and it has a fix
// line for every code the file lists for those requests.

import type { INodeProperties } from 'n8n-workflow';
import { describe, expect, it } from 'vitest';
import { readAnswer } from '../nodes/Status200Uploads/shared/answer';
import {
	API_BASE_URL,
	PLATFORMS,
	REQUIRED_FIELDS,
} from '../nodes/Status200Uploads/shared/constants';
import { FIX_TEXT } from '../nodes/Status200Uploads/shared/fixes';
import { KEY_MAX_LENGTH, KEY_PATTERN } from '../nodes/Status200Uploads/shared/idempotency';
import { ENDPOINTS } from '../nodes/Status200Uploads/shared/request';
import { RETRY_TABLE, retryRuleFor } from '../nodes/Status200Uploads/shared/retry';
import { description } from './support/fake';
import {
	check,
	deref,
	errorCodesOf,
	resolveRef,
	responseExamples,
	spec,
	v2Operation,
	v2Operations,
} from './support/spec';

type Json = Record<string, unknown>;

const OPTION_SCHEMAS: Record<string, string> = {
	tiktok: 'TikTokOptions',
	instagram: 'InstagramOptions',
	facebook: 'FacebookOptions',
	youtube: 'YouTubeOptions',
	x: 'XOptions',
	linkedin: 'LinkedInOptions',
	pinterest: 'PinterestOptions',
	threads: 'ThreadsOptions',
	skool: 'SkoolOptions',
};

function schema(name: string): Json {
	return spec.components.schemas[name];
}

function property(name: string): INodeProperties {
	const found = description.properties.find((p) => p.name === name);
	if (!found) throw new Error(`no property ${name}`);
	return found;
}

function optionValues(p: INodeProperties): string[] {
	return ((p.options ?? []) as Array<{ value?: unknown }>).map((o) => String(o.value)).sort();
}

describe('the requests the node sends exist on the main address', () => {
	it('the base URL is the file’s top-level server', () => {
		expect(spec.servers[0].url).toBe(API_BASE_URL);
	});

	for (const [operation, endpoint] of Object.entries(ENDPOINTS)) {
		it(`${operation}: ${endpoint.method} ${endpoint.path}`, () => {
			const op = v2Operation(endpoint.method, endpoint.path);
			expect(op, `${endpoint.method} ${endpoint.path} is not in the file`).toBeDefined();
			const pathItem = spec.paths[endpoint.path];
			const params = [
				...((pathItem.parameters as unknown[]) ?? []),
				...(((op as Json).parameters as unknown[]) ?? []),
			].map((p) => deref<{ name: string; in: string }>(p));
			const query = params.filter((p) => p.in === 'query').map((p) => p.name);
			for (const q of endpoint.query) expect(query, `query ${q}`).toContain(q);
			if (endpoint.method === 'POST') {
				expect(params.map((p) => p.name)).toContain('Idempotency-Key');
			}
		});
	}

	it('the node uses nothing of the older address', () => {
		for (const endpoint of Object.values(ENDPOINTS)) {
			expect(spec.paths[endpoint.path].servers).toBeUndefined();
		}
	});
});

describe('the fields and choices the node offers are the file’s', () => {
	it('the platform list is components.schemas.Platform', () => {
		expect([...PLATFORMS].sort()).toEqual([...(schema('Platform').enum as string[])].sort());
		expect(optionValues(property('platform'))).toEqual([...PLATFORMS].sort());
	});

	it('each network’s option fields are fields of its option schema', () => {
		for (const [platform, schemaName] of Object.entries(OPTION_SCHEMAS)) {
			const collection = property(`${platform}Options`);
			const names = ((collection.options ?? []) as INodeProperties[]).map((o) => o.name);
			const known = Object.keys(schema(schemaName).properties as Json);
			for (const name of names) expect(known, `${platform}.${name}`).toContain(name);
		}
	});

	it('the node offers no option the file marks as not used', () => {
		for (const [platform, schemaName] of Object.entries(OPTION_SCHEMAS)) {
			const props = schema(schemaName).properties as Record<string, Json>;
			const names = ((property(`${platform}Options`).options ?? []) as INodeProperties[]).map(
				(o) => o.name,
			);
			for (const name of names)
				expect(props[name]['x-status200-not-used'], `${platform}.${name}`).toBeUndefined();
		}
	});

	it('the fields the node shows on their own are the file’s required per-network fields', () => {
		for (const [param, target] of Object.entries(REQUIRED_FIELDS)) {
			expect(
				Object.keys(schema(OPTION_SCHEMAS[target.platform]).properties as Json),
				param,
			).toContain(target.field);
			expect(property(param).required, param).toBe(true);
		}
	});

	it('every fixed list of choices equals the file’s enum', () => {
		const optionsOf = (collection: string, field: string) =>
			optionValues(
				((property(collection).options ?? []) as INodeProperties[]).find(
					(o) => o.name === field,
				) as INodeProperties,
			);
		const enumOf = (schemaName: string, field: string) =>
			[
				...(((schema(schemaName).properties as Record<string, Json>)[field].enum as string[]) ??
					[]),
			].sort();
		expect(optionValues(property('youtubePrivacyStatus'))).toEqual(
			enumOf('YouTubeOptions', 'privacyStatus'),
		);
		expect(optionsOf('youtubeOptions', 'license')).toEqual(enumOf('YouTubeOptions', 'license'));
		expect(optionsOf('instagramOptions', 'postType')).toEqual(
			enumOf('InstagramOptions', 'postType'),
		);
		expect(optionsOf('facebookOptions', 'postType')).toEqual(enumOf('FacebookOptions', 'postType'));
		expect(optionsOf('xOptions', 'whoCanReply')).toEqual(enumOf('XOptions', 'whoCanReply'));
		const statusFilter = resolveRef<Json>('#/components/parameters/StatusFilter');
		const kindFilter = resolveRef<Json>('#/components/parameters/KindFilter');
		const filters = property('filters').options as INodeProperties[];
		expect(optionValues(filters.find((f) => f.name === 'status') as INodeProperties)).toEqual(
			[...((((statusFilter.schema as Json).items as Json).enum as string[]) ?? [])].sort(),
		);
		expect(optionValues(filters.find((f) => f.name === 'kind') as INodeProperties)).toEqual(
			[...(((kindFilter.schema as Json).enum as string[]) ?? [])].sort(),
		);
	});

	it('Get Many reads at most the file’s page size', () => {
		const limit = resolveRef<Json>('#/components/parameters/Limit').schema as Json;
		const nodeLimit = description.properties.find(
			(p) => p.name === 'limit' && p.displayOptions?.show?.resource?.includes('post'),
		);
		expect(nodeLimit?.typeOptions?.maxValue).toBe(limit.maximum);
	});

	it('the Idempotency-Key rules are the file’s', () => {
		const key = resolveRef<Json>('#/components/parameters/IdempotencyKey').schema as Json;
		expect(KEY_MAX_LENGTH).toBe(key.maxLength);
		expect(KEY_PATTERN.source).toBe(key.pattern);
	});
});

describe('the retry table is the file’s', () => {
	const table = spec.components['x-status200-retry'];

	it('components.x-status200-retry equals the node’s table', () => {
		expect(RETRY_TABLE.version).toBe(table.version);
		expect(RETRY_TABLE.by_code).toEqual(table.by_code);
		expect(RETRY_TABLE.by_status).toEqual(table.by_status);
	});

	it('the node knows every rule the file defines', () => {
		expect(Object.keys(table.rules).sort()).toEqual([
			'never',
			'not_a_failure',
			'resend_once_with_key',
			'wait_and_resend',
		]);
	});

	it('the rule of every listed code is the file’s rule, read in the file’s order', () => {
		for (const { op } of v2Operations()) {
			for (const { status, code } of errorCodesOf(op)) {
				const expected = table.by_code[code] ?? table.by_status[`${status[0]}xx`];
				expect(
					retryRuleFor({ status: Number(status), code, json: true }),
					`${status} ${code}`,
				).toBe(expected);
			}
		}
		expect(retryRuleFor({ status: 504, json: false })).toBe(table.by_status.not_json);
	});
});

describe('the node has a fix line for every code of the requests it sends', () => {
	const used = Object.values(ENDPOINTS).map((e) => ({
		e,
		op: v2Operation(e.method, e.path) as Json,
	}));

	it('every x-error-codes code, and every code of the retry table that is not a success', () => {
		const codes = new Set<string>();
		for (const { op } of used) for (const { code } of errorCodesOf(op)) codes.add(code);
		for (const [code, rule] of Object.entries(spec.components['x-status200-retry'].by_code)) {
			if (rule !== 'not_a_failure') codes.add(code);
		}
		for (const code of ['not_found', 'method_not_allowed']) codes.add(code);
		const missing = [...codes].filter((code) => !FIX_TEXT[code]);
		expect(missing).toEqual([]);
	});

	it('the fix lines follow n8n’s wording rules (no "error", "problem", "failure" or "mistake")', () => {
		for (const [code, text] of Object.entries(FIX_TEXT)) {
			expect(text, code).not.toMatch(
				/\b(error|errors|problem|problems|failure|failures|mistake|mistakes)\b/i,
			);
			expect(text.trim(), code).toMatch(/[.)]$/);
		}
	});
});

describe('the file’s example answers are read as the successes they are', () => {
	for (const [name, examples] of [
		['Published', responseExamples('Published')],
		['Accepted', responseExamples('Accepted')],
	] as const) {
		for (const [example, body] of Object.entries(examples)) {
			it(`${name}: ${example}`, () => {
				const status = name === 'Published' ? 200 : 202;
				const pointer = `/components/responses/${name}/content/application~1json/schema`;
				expect(check(pointer, body)).toBe('');
				const answer = readAnswer({ statusCode: status, body });
				expect(retryRuleFor(answer)).toBe('not_a_failure');
				if (body.status200) expect(answer.body?.status200).toEqual(body.status200);
			});
		}
	}

	it('the request examples fit PostRequest the way the node sends them', () => {
		const post = v2Operation('POST', '/posts') as Json;
		const content = ((post.requestBody as Json).content as Json)['application/json'] as Json;
		for (const [name, example] of Object.entries(
			content.examples as Record<string, { value: unknown }>,
		)) {
			expect(check('/components/schemas/PostRequest', example.value), name).toBe('');
		}
	});
});
