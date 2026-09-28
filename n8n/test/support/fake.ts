// A stand-in for the n8n context of one item, close to the real one where it matters:
//   - the node's parameters are resolved with n8n-workflow's own NodeHelpers.getNodeParameters, as the
//     editor stores them (defaults filled in, hidden parameters dropped);
//   - getNodeParameter reads dotted paths, falls back like n8n, and extracts resource locator values
//     with the mode's own extractValue regex;
//   - HTTP goes to a scripted list of answers, and every request n8n would send is recorded.
// runItem() plays n8n's declarative routing for one item: preSend, the request, postReceive.

import {
	NodeHelpers,
	type IDataObject,
	type IExecuteSingleFunctions,
	type IHttpRequestOptions,
	type ILoadOptionsFunctions,
	type INode,
	type INodeExecutionData,
	type INodeParameterResourceLocator,
	type INodeParameters,
	type INodeProperties,
	type IN8nHttpFullResponse,
} from 'n8n-workflow';
import { Status200Uploads } from '../../nodes/Status200Uploads/Status200Uploads.node';
import { handleAnswer, prepareRequest } from '../../nodes/Status200Uploads/shared/hooks';
import { API_BASE_URL, CREDENTIAL_TYPE } from '../../nodes/Status200Uploads/shared/constants';

export const nodeType = new Status200Uploads();
export const description = nodeType.description;

/** A scripted answer: what the server sends, or what the request throws. */
export type Scripted =
	| { status: number; body?: unknown; headers?: Record<string, string> }
	| { throws: unknown };

export class FakeHttp {
	readonly sent: IHttpRequestOptions[] = [];
	readonly credentialTypes: string[] = [];
	private readonly queue: Scripted[] = [];

	answer(...answers: Scripted[]): this {
		this.queue.push(...answers);
		return this;
	}

	get left(): number {
		return this.queue.length;
	}

	async request(
		credentialType: string,
		options: IHttpRequestOptions,
	): Promise<IN8nHttpFullResponse> {
		this.credentialTypes.push(credentialType);
		this.sent.push(JSON.parse(JSON.stringify(options)) as IHttpRequestOptions);
		const next = this.queue.shift();
		if (!next) throw new Error(`no scripted answer for ${options.method} ${options.url}`);
		if ('throws' in next) throw next.throws;
		return {
			statusCode: next.status,
			headers: next.headers ?? {},
			body: (next.body ?? '') as IN8nHttpFullResponse['body'],
		};
	}
}

/** A resource locator value, as the editor stores it. */
export function locator(value: string, mode = 'list'): INodeParameterResourceLocator {
	return { __rl: true, mode, value };
}

function modeOf(name: string, mode: string): { extractValue?: { regex: string } } | undefined {
	for (const p of description.properties) {
		if (p.name === name && p.type === 'resourceLocator') {
			return (p.modes ?? []).find((m) => m.name === mode) as
				| { extractValue?: { regex: string } }
				| undefined;
		}
	}
	return undefined;
}

function valueAt(params: INodeParameters, path: string): unknown {
	let at: unknown = params;
	for (const part of path.split('.')) {
		if (at === null || typeof at !== 'object') return undefined;
		at = (at as IDataObject)[part];
	}
	return at;
}

function extract(name: string, value: unknown): unknown {
	if (value === null || typeof value !== 'object' || !(value as IDataObject).__rl) return value;
	const rl = value as { mode: string; value: string };
	const regex = modeOf(name, rl.mode)?.extractValue?.regex;
	if (!regex) return rl.value;
	const m = new RegExp(regex).exec(String(rl.value));
	return m ? m[1] : rl.value;
}

/** The parameters the editor would store for these user choices. */
/** Parameters as a test writes them (resource locators, collections, plain values). */
export type UserParameters = Record<string, unknown>;

export function resolveParameters(user: UserParameters): INodeParameters {
	return (
		NodeHelpers.getNodeParameters(
			description.properties as INodeProperties[],
			user as INodeParameters,
			true,
			false,
			{ typeVersion: 1 },
			description,
		) ?? {}
	);
}

export interface ItemOptions {
	itemIndex?: number;
	executionId?: string;
	workflowId?: string;
	timezone?: string;
	signal?: AbortSignal;
	/**
	 * Parameters whose expression gives a new value on every read, as n8n evaluates {{ $now }} again
	 * on each getNodeParameter call: the function is called on every read.
	 */
	volatile?: Record<string, () => unknown>;
}

export const TEST_NODE_ID = '5b0a4f1e-1111-4222-8333-944455556666';

export function makeNode(parameters: INodeParameters): INode {
	return {
		id: TEST_NODE_ID,
		name: 'Status 200 Uploads',
		type: '@status200uploads/n8n-nodes-status200uploads.status200Uploads',
		typeVersion: 1,
		position: [0, 0],
		parameters,
		credentials: { status200UploadsApi: { id: '1', name: 'Status 200 Uploads account' } },
	};
}

/** The context n8n hands to preSend and postReceive for one item. */
export function itemContext(
	user: UserParameters,
	http: FakeHttp,
	options: ItemOptions = {},
): IExecuteSingleFunctions {
	const parameters = resolveParameters(user);
	const node = makeNode(parameters);
	const ctx = {
		getNodeParameter(name: string, fallback?: unknown, opts?: { extractValue?: boolean }) {
			const fresh = options.volatile?.[name];
			if (fresh) return fresh();
			let value = valueAt(parameters, name);
			if (opts?.extractValue) value = extract(name, value);
			if (value === undefined) {
				if (fallback === undefined) throw new Error(`Could not get parameter "${name}"`);
				return fallback;
			}
			return value;
		},
		getNode: () => node,
		getWorkflow: () => ({ id: options.workflowId ?? 'wf-test', name: 'Test', active: false }),
		getExecutionId: () => options.executionId ?? 'exec-1',
		getItemIndex: () => options.itemIndex ?? 0,
		getTimezone: () => options.timezone ?? 'UTC',
		getExecutionCancelSignal: () => options.signal,
		helpers: {
			httpRequestWithAuthentication: async (type: string, requestOptions: IHttpRequestOptions) =>
				await http.request(type, requestOptions),
		},
	};
	return ctx as unknown as IExecuteSingleFunctions;
}

/** The context n8n hands to listSearch and loadOptions methods in the editor. */
export function editorContext(user: UserParameters, http: FakeHttp): ILoadOptionsFunctions {
	const parameters = resolveParameters(user);
	const node = makeNode(parameters);
	const ctx = {
		getCurrentNodeParameter(name: string, opts?: { extractValue?: boolean }) {
			const value = valueAt(parameters, name);
			return opts?.extractValue ? extract(name, value) : value;
		},
		getNodeParameter(name: string, fallback?: unknown) {
			return valueAt(parameters, name) ?? fallback;
		},
		getNode: () => node,
		getTimezone: () => 'UTC',
		helpers: {
			httpRequestWithAuthentication: async (type: string, requestOptions: IHttpRequestOptions) =>
				await http.request(type, requestOptions),
		},
	};
	return ctx as unknown as ILoadOptionsFunctions;
}

/**
 * One item through n8n's declarative routing, as n8n-core's RoutingNode runs it: the defaults and the
 * operation's request, then preSend, then the request itself (httpRequestWithAuthentication with
 * returnFullResponse), then postReceive with that full response.
 */
export async function runItem(
	ctx: IExecuteSingleFunctions,
	http: FakeHttp,
): Promise<INodeExecutionData[]> {
	const start: IHttpRequestOptions = {
		baseURL: API_BASE_URL,
		url: '',
		qs: {},
		body: {},
		headers: { ...(description.requestDefaults?.headers as IDataObject) },
		timeout: 300000,
	};
	const options = await prepareRequest.call(ctx, start);
	options.returnFullResponse = true;
	const response = await http.request(CREDENTIAL_TYPE, options);
	return await handleAnswer.call(ctx, [{ json: response.body as IDataObject }], response);
}

/** A post body answer of the API with a JSON body. */
export function json(
	status: number,
	body: unknown,
	headers: Record<string, string> = {},
): Scripted {
	return { status, body, headers: { 'content-type': 'application/json', ...headers } };
}
