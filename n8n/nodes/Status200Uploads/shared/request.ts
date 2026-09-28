import type { IDataObject } from 'n8n-workflow';
import { LIST_FIELDS, PLATFORMS, REQUIRED_FIELDS, UUID_PATTERN, type Platform } from './constants';
import { automaticKey, checkCustomKey, type KeyInputs } from './idempotency';
import { InvalidInput } from './input';
import { scheduledForValue } from './time';

/** Every operation of the node, as resource.operation. */
export type Operation =
	| 'account.getAll'
	| 'account.getPostingOptions'
	| 'media.get'
	| 'media.importFromUrl'
	| 'post.cancel'
	| 'post.create'
	| 'post.get'
	| 'post.getAll';

export type HttpMethod = 'GET' | 'POST' | 'DELETE';

/**
 * The requests this node sends: the method, the path under https://status200uploads.com/api/v2 (as the
 * OpenAPI file writes it) and the query parameters it may use. test/contract.test.ts holds each to the
 * file.
 */
export const ENDPOINTS: Record<Operation, { method: HttpMethod; path: string; query: string[] }> = {
	'account.getAll': { method: 'GET', path: '/accounts', query: [] },
	'account.getPostingOptions': {
		method: 'GET',
		path: '/accounts/{profile_id}/options',
		query: ['platforms', 'skool_group_slug'],
	},
	'media.get': { method: 'GET', path: '/media', query: ['file_id'] },
	'media.importFromUrl': { method: 'POST', path: '/media', query: [] },
	'post.cancel': { method: 'DELETE', path: '/posts/{id}', query: [] },
	'post.create': { method: 'POST', path: '/posts', query: [] },
	'post.get': { method: 'GET', path: '/posts/{id}', query: [] },
	'post.getAll': {
		method: 'GET',
		path: '/posts',
		query: ['limit', 'cursor', 'status', 'platform', 'kind', 'profile_id'],
	},
};

/** Reads a parameter of the current item (a resource locator gives its value). */
export interface ParamReader {
	get(name: string, fallback: unknown): unknown;
}

/** What the request needs beyond the parameters. */
export interface RequestEnv extends KeyInputs {
	/** The workflow's time zone (n8n's getTimezone). */
	timezone: string;
}

/** One request, complete: preSend sends it, and a resend sends exactly the same. */
export interface ApiRequest {
	operation: Operation;
	method: HttpMethod;
	/** The path under /api/v2, ids filled in. */
	url: string;
	qs: IDataObject;
	body?: IDataObject;
	headers: Record<string, string>;
	/** An Idempotency-Key is on the request. */
	keySent: boolean;
	/** Sending it twice changes nothing (a read, a cancel, a dry run). */
	repeatable: boolean;
}

const NOT_JSON = Symbol('not JSON');
const UUID = new RegExp(`^${UUID_PATTERN}$`);
const UUID_IN_POST_URL = new RegExp(`/posts/(${UUID_PATTERN})`);

function isPlainObject(value: unknown): value is IDataObject {
	return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function str(value: unknown): string {
	if (typeof value === 'string') return value.trim();
	if (typeof value === 'number' || typeof value === 'boolean') return String(value);
	return '';
}

/** A list from text (split on the separator) or from a list an expression gave. */
export function splitList(value: unknown, separator: RegExp): string[] {
	const parts = Array.isArray(value) ? value.map((v) => str(v)) : str(value).split(separator);
	return parts.map((p) => p.trim()).filter((p) => p !== '');
}

/** The operation the parameters name. */
export function operationOf(p: ParamReader): Operation {
	const operation = `${str(p.get('resource', 'post'))}.${str(p.get('operation', ''))}`;
	if (Object.prototype.hasOwnProperty.call(ENDPOINTS, operation)) return operation as Operation;
	throw new InvalidInput(
		`The operation "${operation}" is not known`,
		'Choose a resource and an operation of this node',
	);
}

/** An id of this API (a UUID), also read from a pasted status_url (…/api/v2/posts/<id>). */
export function idFrom(value: unknown, what: string, hint: string): string {
	const text = str(value);
	const inUrl = UUID_IN_POST_URL.exec(text);
	if (inUrl) return inUrl[1].toLowerCase();
	if (UUID.test(text)) return text.toLowerCase();
	if (text === '') throw new InvalidInput(`${what} is empty`, hint);
	throw new InvalidInput(`${what} is not an ID of Status 200 Uploads`, hint);
}

function mergeDeep(target: IDataObject, extra: IDataObject): IDataObject {
	for (const [key, value] of Object.entries(extra)) {
		const current = target[key];
		target[key] =
			isPlainObject(current) && isPlainObject(value) ? mergeDeep({ ...current }, value) : value;
	}
	return target;
}

function additionalPostFields(value: unknown): IDataObject {
	if (value === undefined || value === null || value === '') return {};
	if (isPlainObject(value)) return value;
	if (typeof value === 'string') {
		if (value.trim() === '') return {};
		let parsed: unknown = NOT_JSON;
		try {
			parsed = JSON.parse(value);
		} catch {
			parsed = NOT_JSON;
		}
		if (parsed === NOT_JSON) {
			throw new InvalidInput(
				'Additional Post Fields is not valid JSON',
				'Write a JSON object, for example {"tiktok": {"isAiGenerated": true}}',
			);
		}
		if (isPlainObject(parsed)) return parsed;
	}
	throw new InvalidInput(
		'Additional Post Fields is not a JSON object',
		'Write a JSON object, for example {"tiktok": {"isAiGenerated": true}}',
	);
}

/** One network's option block: empty fields left out, list fields split on commas. */
function optionBlock(platform: Platform, raw: unknown): IDataObject {
	const block: IDataObject = {};
	if (!isPlainObject(raw)) return block;
	for (const [key, value] of Object.entries(raw)) {
		if (value === undefined || value === null || value === '') continue;
		if (LIST_FIELDS[platform]?.includes(key)) {
			const list = splitList(value, /,/);
			if (list.length > 0) block[key] = list;
			continue;
		}
		block[key] = typeof value === 'string' ? value.trim() : value;
	}
	return block;
}

/** The body of POST /posts: {post, dryRun?}. */
export function buildPostBody(p: ParamReader, env: RequestEnv): IDataObject {
	const platform = str(p.get('platform', '')) as Platform;
	if (!PLATFORMS.includes(platform)) {
		throw new InvalidInput(
			`The platform "${platform}" is not known`,
			`Choose one of: ${PLATFORMS.join(', ')}`,
		);
	}
	const accountId = str(p.get('account', ''));
	if (accountId === '') {
		throw new InvalidInput(
			'Account is empty',
			'Choose the account from the list, or give its ID or its @handle',
		);
	}
	const post: IDataObject = { accountId, platform };

	const content: IDataObject = {};
	const text = p.get('text', '');
	if (typeof text === 'string' ? text !== '' : text !== undefined && text !== null)
		content.text = String(text);
	const media = str(p.get('media', 'none'));
	if (media === 'urls') {
		const urls = splitList(p.get('mediaUrls', ''), /\s+/);
		if (urls.length === 0)
			throw new InvalidInput(
				'Media URLs is empty',
				'Give one public URL per line, or set Media to None',
			);
		content.mediaUrls = urls;
	} else if (media === 'fileIds') {
		const ids = splitList(p.get('fileIds', ''), /[\s,]+/);
		if (ids.length === 0)
			throw new InvalidInput(
				'File IDs is empty',
				'Give the file_id of Media: Import From URL, or set Media to None',
			);
		content.mediaID = ids;
	}
	if (Object.keys(content).length > 0) post.content = content;

	if (str(p.get('when', 'now')) === 'later') {
		post.scheduledFor = scheduledForValue(p.get('scheduledFor', ''), env.timezone);
	}

	const block: IDataObject = {};
	for (const [param, target] of Object.entries(REQUIRED_FIELDS)) {
		if (target.platform !== platform) continue;
		const value = str(p.get(param, ''));
		if (value !== '') block[target.field] = value;
	}
	Object.assign(block, optionBlock(platform, p.get(`${platform}Options`, {})));
	if (Object.keys(block).length > 0) post[platform] = block;

	mergeDeep(post, additionalPostFields(p.get('options.additionalPostFields', '')));

	const body: IDataObject = { post };
	if (p.get('options.dryRun', false) === true) body.dryRun = true;
	return body;
}

/** The Idempotency-Key header of a POST, by the Idempotency Key option. */
function keyHeader(p: ParamReader, env: RequestEnv, body: IDataObject): Record<string, string> {
	const mode = str(p.get('options.idempotencyKeyMode', 'auto')) || 'auto';
	if (mode === 'off') return {};
	if (mode === 'custom') {
		const checked = checkCustomKey(p.get('options.customIdempotencyKey', ''));
		if ('reason' in checked) {
			throw new InvalidInput(
				checked.reason,
				'Use 1 to 255 printable ASCII characters, for example an expression such as {{ $json.id }}-tiktok, or set Idempotency Key to Automatic',
			);
		}
		return { 'Idempotency-Key': checked.key };
	}
	return { 'Idempotency-Key': automaticKey(env, body) };
}

function request(operation: Operation, url: string, parts: Partial<ApiRequest> = {}): ApiRequest {
	const method = ENDPOINTS[operation].method;
	return {
		operation,
		method,
		url,
		qs: {},
		headers: {},
		keySent: false,
		repeatable: method !== 'POST',
		...parts,
	};
}

/** The complete request of the current item. */
export function buildRequest(p: ParamReader, env: RequestEnv): ApiRequest {
	const operation = operationOf(p);
	switch (operation) {
		case 'account.getAll':
			return request(operation, '/accounts');

		case 'account.getPostingOptions': {
			const id = idFrom(
				p.get('profile', ''),
				'Account',
				'Choose the account from the list, or give its ID (profile_id of Account: Get Many)',
			);
			const qs: IDataObject = {};
			const platforms = splitList(p.get('platforms', []), /,/);
			if (platforms.length > 0) qs.platforms = platforms.join(',');
			const slug = str(p.get('skoolGroupSlug', ''));
			if (slug !== '') qs.skool_group_slug = slug;
			return request(operation, `/accounts/${id}/options`, { qs });
		}

		case 'post.create': {
			const body = buildPostBody(p, env);
			if (body.dryRun === true) {
				// A dry run sends nothing and ignores the key: no key, and safe to send again.
				return request(operation, '/posts', { body, repeatable: true });
			}
			const headers = keyHeader(p, env, body);
			return request(operation, '/posts', { body, headers, keySent: 'Idempotency-Key' in headers });
		}

		case 'post.get': {
			const id = idFrom(
				p.get('post', ''),
				'Post',
				'Use status200.post_id, status200.scheduled_post_id or status200.status_url of a Create answer',
			);
			return request(operation, `/posts/${id}`);
		}

		case 'post.getAll': {
			const returnAll = p.get('returnAll', false) === true;
			const limit = Math.min(100, Math.max(1, Math.floor(Number(p.get('limit', 50)) || 50)));
			const qs: IDataObject = { limit: returnAll ? 100 : limit };
			const filters = p.get('filters', {});
			if (isPlainObject(filters)) {
				const statuses = splitList(filters.status, /,/);
				if (statuses.length > 0) qs.status = statuses.join(',');
				if (str(filters.platform) !== '') qs.platform = str(filters.platform);
				if (str(filters.kind) !== '') qs.kind = str(filters.kind);
				if (str(filters.profileId) !== '') qs.profile_id = str(filters.profileId);
			}
			return request(operation, '/posts', { qs });
		}

		case 'post.cancel': {
			const id = idFrom(
				p.get('scheduledPost', ''),
				'Scheduled Post',
				'Use scheduled_post_id of a scheduled or queued Create answer, or choose the post from the list',
			);
			return request(operation, `/posts/${id}`);
		}

		case 'media.importFromUrl': {
			const url = str(p.get('url', ''));
			if (url === '')
				throw new InvalidInput(
					'URL is empty',
					'Give the public http or https URL of the image or video file',
				);
			const body: IDataObject = { url };
			const headers = keyHeader(p, env, body);
			return request(operation, '/media', { body, headers, keySent: 'Idempotency-Key' in headers });
		}

		case 'media.get': {
			const id = idFrom(p.get('fileId', ''), 'File ID', 'Use file_id of Media: Import From URL');
			return request(operation, '/media', { qs: { file_id: id } });
		}
	}
}
