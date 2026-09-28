import type { IDataObject } from 'n8n-workflow';

/**
 * The fields Simplify keeps of a post or a scheduled post (GET /posts and GET /posts/{id}). A post has
 * at most nine of them and a scheduled post at most nine, within n8n's limit of ten.
 */
export const SIMPLE_POST_FIELDS = [
	'id',
	'kind',
	'platform',
	'platforms',
	'status',
	'outcome',
	'done',
	'permalink',
	'error_message',
	'at',
	'scheduled_post_id',
	'results',
] as const;

function isPlainObject(value: unknown): value is IDataObject {
	return typeof value === 'object' && value !== null && !Array.isArray(value);
}

/** A post or scheduled post with only the fields Simplify keeps. */
export function simplifyPost(item: unknown): IDataObject {
	if (!isPlainObject(item)) return {};
	const out: IDataObject = {};
	for (const field of SIMPLE_POST_FIELDS) {
		if (Object.prototype.hasOwnProperty.call(item, field)) out[field] = item[field];
	}
	return out;
}

/** The objects of a list answer's data. */
export function dataList(body: IDataObject | null): IDataObject[] {
	const data = body?.data;
	return Array.isArray(data) ? data.filter(isPlainObject) : [];
}

/** The object of a one-item answer's data (or the body itself when there is no data). */
export function dataObject(body: IDataObject | null): IDataObject {
	const data = body?.data;
	return isPlainObject(data) ? data : (body ?? {});
}
