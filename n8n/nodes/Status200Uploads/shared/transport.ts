import { randomUUID } from 'crypto';
import {
	NodeApiError,
	NodeOperationError,
	sleep,
	type IDataObject,
	type IExecuteSingleFunctions,
	type IHttpRequestOptions,
	type ILoadOptionsFunctions,
	type JsonObject,
} from 'n8n-workflow';
import { noAnswer, readAnswer, type Answer, type FullResponse } from './answer';
import { API_BASE_URL, CREDENTIAL_TYPE, USER_AGENT } from './constants';
import { describeFailure, failureMessage, type RequestKind } from './fixes';
import { InvalidInput } from './input';
import { buildRequest, type ApiRequest, type ParamReader, type RequestEnv } from './request';
import { settle, type Settled } from './retry';

type Context = IExecuteSingleFunctions | ILoadOptionsFunctions;

/** The headers of every request; the credential adds Authorization. */
export const DEFAULT_HEADERS: Record<string, string> = {
	Accept: 'application/json',
	'Content-Type': 'application/json',
	'User-Agent': USER_AGENT,
};

/** Parameters that are resource locators: read by their value. */
const LOCATOR_PARAMETERS = new Set(['account', 'profile', 'post', 'scheduledPost']);

/** Reads the current item's parameters. */
export function readerOf(fns: IExecuteSingleFunctions): ParamReader {
	return {
		get: (name, fallback) =>
			LOCATOR_PARAMETERS.has(name)
				? fns.getNodeParameter(name, fallback, { extractValue: true })
				: fns.getNodeParameter(name, fallback),
	};
}

/**
 * A stand-in execution id per item for a run that has none, shared by the request and its resends
 * (n8n hands the same context object to preSend and postReceive).
 */
const standInExecutionIds = new WeakMap<object, string>();

/** What the request needs beyond the parameters: the time zone and what makes the automatic key. */
export function envOf(fns: IExecuteSingleFunctions): RequestEnv {
	let executionId = String(fns.getExecutionId() ?? '');
	if (executionId === '') {
		let standIn = standInExecutionIds.get(fns);
		if (standIn === undefined) {
			standIn = `no-execution-id-${randomUUID()}`;
			standInExecutionIds.set(fns, standIn);
			fns.logger?.warn(
				'Status 200 Uploads: this run has no execution id, so the automatic Idempotency-Key is random for this item: Retry On Fail cannot replay it. Use a Custom Idempotency Key to be safe.',
			);
		}
		executionId = standIn;
	}
	const node = fns.getNode();
	return {
		workflowId: String(fns.getWorkflow()?.id ?? ''),
		executionId,
		nodeId: String(node.id ?? node.name),
		itemIndex: fns.getItemIndex(),
		timezone: fns.getTimezone(),
	};
}

/**
 * The request preSend built for an item, kept for its postReceive (n8n hands the same context object
 * to both). A resend must be this very request: reading the parameters again would evaluate their
 * expressions again, and a field such as {{ $now }} would give a new body and a new automatic key.
 */
const preparedRequests = new WeakMap<object, ApiRequest>();

/** Keeps the request preSend built for this item (called by preSend). */
export function keepRequest(fns: object, req: ApiRequest): void {
	preparedRequests.set(fns, req);
}

/** The request preSend built for this item; built from the parameters only when there is none. */
export function preparedRequestOf(fns: IExecuteSingleFunctions): ApiRequest {
	return preparedRequests.get(fns) ?? requestOf(fns);
}

/** The current item's request, or a NodeOperationError that says which parameter to change. */
export function requestOf(fns: IExecuteSingleFunctions): ApiRequest {
	const itemIndex = fns.getItemIndex();
	try {
		return buildRequest(readerOf(fns), envOf(fns));
	} catch (error) {
		if (error instanceof InvalidInput) {
			throw new NodeOperationError(fns.getNode(), `${error.message} [item ${itemIndex}]`, {
				description: error.description,
				itemIndex,
			});
		}
		throw new NodeOperationError(fns.getNode(), error as Error, { itemIndex });
	}
}

/** The n8n request options of a request (the base URL, the node's headers, never an HTTP-status throw). */
export function httpOptionsOf(
	req: ApiRequest,
	base: Partial<IHttpRequestOptions> = {},
): IHttpRequestOptions {
	const options: IHttpRequestOptions = {
		...base,
		baseURL: base.baseURL ?? API_BASE_URL,
		url: req.url,
		method: req.method,
		qs: { ...req.qs },
		headers: {
			...((base.headers as IDataObject | undefined) ?? {}),
			...DEFAULT_HEADERS,
			...req.headers,
		},
		json: true,
		returnFullResponse: true,
		ignoreHttpStatusErrors: true,
	};
	if (req.body !== undefined) options.body = req.body;
	else delete options.body;
	return options;
}

/**
 * The transport settings n8n put on the item's first request (the node's Request Options: timeout,
 * proxy, certificate check; the credential's allowed domains). preSend keeps them so that a resend,
 * a next page or an import status read travels exactly like the first request.
 */
const TRANSPORT_KEYS = [
	'timeout',
	'proxy',
	'skipSslCertificateValidation',
	'allowedDomains',
	'sendCredentialsOnCrossOriginRedirect',
] as const;
const transportSettings = new WeakMap<object, Partial<IHttpRequestOptions>>();

/** Keeps the transport settings of the item's first request (called by preSend). */
export function keepTransportSettings(fns: object, options: Partial<IHttpRequestOptions>): void {
	const kept: Partial<IHttpRequestOptions> = {};
	for (const key of TRANSPORT_KEYS) {
		if (options[key] !== undefined)
			(kept as IDataObject)[key] = options[key] as IDataObject[string];
	}
	transportSettings.set(fns, kept);
}

/** Error codes of a connection that broke, timed out or never opened: no answer arrived. */
const NO_ANSWER_CODES = new Set([
	'ECONNRESET',
	'ECONNABORTED',
	'ECONNREFUSED',
	'ETIMEDOUT',
	'ESOCKETTIMEDOUT',
	'EPIPE',
	'EAI_AGAIN',
	'ENOTFOUND',
	'ENETUNREACH',
	'EHOSTUNREACH',
	'ERR_SOCKET_CONNECTION_TIMEOUT',
	'UND_ERR_SOCKET',
	'UND_ERR_CONNECT_TIMEOUT',
	'UND_ERR_HEADERS_TIMEOUT',
	'UND_ERR_BODY_TIMEOUT',
]);

/** Whether a thrown request means that no answer arrived (n8n wraps it in a NodeApiError). */
export function isNoAnswer(error: unknown): boolean {
	let current: unknown = error;
	for (let depth = 0; depth < 4 && current !== null && typeof current === 'object'; depth++) {
		const e = current as {
			code?: unknown;
			isAxiosError?: unknown;
			response?: unknown;
			cause?: unknown;
		};
		if (typeof e.code === 'string' && NO_ANSWER_CODES.has(e.code)) return true;
		if (e.isAxiosError === true && e.response === undefined) return true;
		current = e.cause;
	}
	return false;
}

function cancelled(fns: Context): boolean {
	return 'getExecutionCancelSignal' in fns && fns.getExecutionCancelSignal()?.aborted === true;
}

/**
 * Waits, in steps of at most a second, so that a cancelled execution stops the node at once (n8n
 * Cloud allows only n8n-workflow's sleep, which cannot be interrupted).
 */
export async function waitMs(fns: Context, ms: number): Promise<void> {
	let left = ms;
	while (left > 0) {
		if (cancelled(fns))
			throw new NodeOperationError(
				fns.getNode(),
				'The execution was cancelled while the node was waiting',
			);
		const step = Math.min(1000, left);
		await sleep(step);
		left -= step;
	}
}

/**
 * Sends one request and reads its answer. Every HTTP status is an answer; a request that got no
 * answer is the Answer with status 0. Anything else (the execution was cancelled, the credential is
 * missing) stops the node.
 */
export async function sendApiRequest(this: Context, req: ApiRequest): Promise<Answer> {
	let response: unknown;
	try {
		response = await this.helpers.httpRequestWithAuthentication.call(
			this,
			CREDENTIAL_TYPE,
			httpOptionsOf(req, transportSettings.get(this) ?? {}),
		);
	} catch (error) {
		if (!cancelled(this) && isNoAnswer(error)) {
			return noAnswer(error instanceof Error ? error.message : String(error));
		}
		if (error instanceof NodeOperationError) throw new NodeOperationError(this.getNode(), error);
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
	return readAnswer(response as FullResponse);
}

/** How the node waits and resends for one request. */
export interface Policy {
	kind: RequestKind;
	waitWhenAsked: boolean;
	maxWaitSeconds: number;
}

/** The NodeApiError of an answer the node stops at. */
export function failureError(
	fns: Context,
	settled: Settled,
	policy: Policy,
	itemIndex?: number,
): NodeApiError {
	const answer = settled.answer;
	// A body that is not JSON (a gateway's page) or no answer at all: its text, never a made-up status.
	const payload: JsonObject = answer.body
		? (answer.body as JsonObject)
		: answer.status > 0
			? { page: answer.text }
			: { reason: answer.text };
	return new NodeApiError(fns.getNode(), payload, {
		message:
			itemIndex === undefined
				? failureMessage(answer)
				: `${failureMessage(answer)} [item ${itemIndex}]`,
		description: describeFailure(settled, policy.kind, policy.maxWaitSeconds),
		httpCode: answer.status > 0 ? String(answer.status) : undefined,
		itemIndex,
	});
}

/**
 * Follows the retry table from a first answer: the settled answer with the seconds waited for it, or a
 * NodeApiError.
 */
export async function settleOrThrow(
	fns: Context,
	req: ApiRequest,
	first: Answer,
	policy: Policy,
	itemIndex?: number,
): Promise<Settled> {
	const settled = await settle(first, {
		send: async () => await sendApiRequest.call(fns, req),
		sleep: async (ms) => await waitMs(fns, ms),
		keySent: req.keySent,
		repeatable: req.repeatable,
		waitWhenAsked: policy.waitWhenAsked,
		maxWaitSeconds: policy.maxWaitSeconds,
	});
	if (!settled.ok) throw failureError(fns, settled, policy, itemIndex);
	return settled;
}

/** Follows the retry table from a first answer; the final answer, or a NodeApiError. */
export async function settleAnswer(
	fns: Context,
	req: ApiRequest,
	first: Answer,
	policy: Policy,
	itemIndex?: number,
): Promise<Answer> {
	return (await settleOrThrow(fns, req, first, policy, itemIndex)).answer;
}

/** Sends a request and follows the retry table: the final answer, or a NodeApiError. */
export async function call(
	fns: Context,
	req: ApiRequest,
	policy: Policy,
	itemIndex?: number,
): Promise<Answer> {
	const first = await sendApiRequest.call(fns, req);
	return await settleAnswer(fns, req, first, policy, itemIndex);
}
