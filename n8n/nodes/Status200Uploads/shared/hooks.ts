import {
	NodeApiError,
	type IDataObject,
	type IExecuteSingleFunctions,
	type IHttpRequestOptions,
	type IN8nHttpFullResponse,
	type INodeExecutionData,
	type JsonObject,
} from 'n8n-workflow';
import { readAnswer, type Answer, type FullResponse } from './answer';
import {
	DEFAULT_MAX_WAIT_SECONDS,
	MAX_WAIT_LIMIT_SECONDS,
	MEDIA_POLL_SECONDS,
	READ_MAX_WAIT_SECONDS,
} from './constants';
import { FIX_TEXT } from './fixes';
import { dataList, dataObject, simplifyPost } from './output';
import type { ApiRequest } from './request';
import {
	call,
	httpOptionsOf,
	keepRequest,
	keepTransportSettings,
	preparedRequestOf,
	requestOf,
	settleOrThrow,
	waitMs,
	type Policy,
} from './transport';

/**
 * preSend of every operation: the whole request (URL, query, body, headers, Idempotency-Key) is built
 * once, by requestOf, and kept for this item. handleAnswer resends that kept request, so a resend is
 * byte for byte the same even when a field's expression gives a new value on every read ($now).
 * n8n's transport settings on it (timeout, proxy, allowed domains) are kept for the follow-up requests.
 */
export async function prepareRequest(
	this: IExecuteSingleFunctions,
	requestOptions: IHttpRequestOptions,
): Promise<IHttpRequestOptions> {
	const request = requestOf(this);
	keepRequest(this, request);
	keepTransportSettings(this, requestOptions);
	return httpOptionsOf(request, requestOptions);
}

function clampWait(value: unknown): number {
	const n = Number(value);
	if (!Number.isFinite(n)) return DEFAULT_MAX_WAIT_SECONDS;
	return Math.min(MAX_WAIT_LIMIT_SECONDS, Math.max(0, Math.floor(n)));
}

/** How the node waits for this item: from Options on a post or an import, fixed on reads. */
function policyOf(fns: IExecuteSingleFunctions, req: ApiRequest): Policy {
	if (req.operation === 'post.create' || req.operation === 'media.importFromUrl') {
		return {
			kind: req.operation === 'post.create' ? 'post' : 'media',
			waitWhenAsked: fns.getNodeParameter('options.waitWhenAsked', true) !== false,
			maxWaitSeconds: clampWait(fns.getNodeParameter('options.maxWait', DEFAULT_MAX_WAIT_SECONDS)),
		};
	}
	return { kind: 'read', waitWhenAsked: true, maxWaitSeconds: READ_MAX_WAIT_SECONDS };
}

const READ_POLICY: Policy = {
	kind: 'read',
	waitWhenAsked: true,
	maxWaitSeconds: READ_MAX_WAIT_SECONDS,
};

/** Every page of GET /posts after the first, while Return All is on. */
async function remainingPages(
	fns: IExecuteSingleFunctions,
	req: ApiRequest,
	first: Answer,
	itemIndex: number,
): Promise<IDataObject[]> {
	const items: IDataObject[] = [];
	const seen = new Set<string>();
	let cursor = first.body?.next_cursor;
	while (typeof cursor === 'string' && cursor !== '' && !seen.has(cursor)) {
		seen.add(cursor);
		const page = await call(fns, { ...req, qs: { ...req.qs, cursor } }, READ_POLICY, itemIndex);
		items.push(...dataList(page.body));
		cursor = page.body?.next_cursor;
	}
	return items;
}

/**
 * Media: Import From URL with Wait Until Ready: reads GET /media?file_id= every few seconds until the
 * file is ready, within what is left of Max Wait after the import's own waits (alreadyWaited). A file
 * that failed to import stops the node; one still importing when Max Wait passes is output as it is
 * (Post: Create waits for it when it is used).
 */
async function waitUntilReady(
	fns: IExecuteSingleFunctions,
	imported: IDataObject,
	policy: Policy,
	itemIndex: number,
	alreadyWaited: number,
): Promise<IDataObject> {
	const fileId = imported.file_id;
	if (imported.status !== 'processing' || typeof fileId !== 'string') return imported;
	const statusRequest: ApiRequest = {
		operation: 'media.get',
		method: 'GET',
		url: '/media',
		qs: { file_id: fileId },
		headers: {},
		keySent: false,
		repeatable: true,
	};
	let last: IDataObject = imported;
	let waited = alreadyWaited;
	while (waited + MEDIA_POLL_SECONDS <= policy.maxWaitSeconds) {
		await waitMs(fns, MEDIA_POLL_SECONDS * 1000);
		waited += MEDIA_POLL_SECONDS;
		last = (await call(fns, statusRequest, READ_POLICY, itemIndex)).body ?? last;
		if (last.status === 'ready') return last;
		if (last.status === 'failed') {
			const reason = typeof last.error === 'string' && last.error !== '' ? `: ${last.error}` : '';
			throw new NodeApiError(fns.getNode(), last as JsonObject, {
				message: `The import of the file did not finish${reason} [item ${itemIndex}]`,
				description: `${FIX_TEXT.media_failed} File ID: ${fileId}.`,
				itemIndex,
			});
		}
	}
	return last;
}

/**
 * postReceive of every operation: reads the answer, waits and sends the identical request again only
 * where components.x-status200-retry allows it, stops with a NodeApiError that says how to fix it,
 * and outputs the result.
 */
export async function handleAnswer(
	this: IExecuteSingleFunctions,
	_items: INodeExecutionData[],
	response: IN8nHttpFullResponse,
): Promise<INodeExecutionData[]> {
	const itemIndex = this.getItemIndex();
	// The request preSend built and sent, never one read again from the parameters.
	const req = preparedRequestOf(this);
	const policy = policyOf(this, req);
	const settled = await settleOrThrow(
		this,
		req,
		readAnswer(response as FullResponse),
		policy,
		itemIndex,
	);
	const answer = settled.answer;
	const body = answer.body ?? {};
	const pairedItem = { item: itemIndex };
	const simplify = (): boolean => this.getNodeParameter('simplify', true) !== false;

	let out: IDataObject[];
	switch (req.operation) {
		case 'post.create':
			out = [answer.replayed ? { ...body, replayed: true } : body];
			break;
		case 'post.get': {
			const data = dataObject(answer.body);
			out = [simplify() ? simplifyPost(data) : data];
			break;
		}
		case 'post.getAll': {
			const all = dataList(answer.body);
			if (this.getNodeParameter('returnAll', false) === true) {
				all.push(...(await remainingPages(this, req, answer, itemIndex)));
			}
			out = simplify() ? all.map((item) => simplifyPost(item)) : all;
			break;
		}
		case 'account.getAll': {
			const accounts = dataList(answer.body);
			const returnAll = this.getNodeParameter('returnAll', false) === true;
			out = returnAll
				? accounts
				: accounts.slice(0, Number(this.getNodeParameter('limit', 50)) || 50);
			break;
		}
		case 'media.importFromUrl':
			out = [
				this.getNodeParameter('options.waitUntilReady', true) !== false
					? await waitUntilReady(this, body, policy, itemIndex, settled.waitedSeconds)
					: body,
			];
			break;
		case 'media.get':
			out = [body];
			break;
		default:
			// post.cancel and account.getPostingOptions: the answer's data.
			out = [dataObject(answer.body)];
	}
	return out.map((json) => ({ json, pairedItem }));
}
