import { NodeHelpers, type INodeProperties, type INodePropertyOptions } from 'n8n-workflow';
import { describe, expect, it } from 'vitest';
import { Status200UploadsApi } from '../credentials/Status200UploadsApi.credentials';
import {
	API_BASE_URL,
	CREDENTIAL_TYPE,
	USER_AGENT,
} from '../nodes/Status200Uploads/shared/constants';
import { handleAnswer, prepareRequest } from '../nodes/Status200Uploads/shared/hooks';
import { ENDPOINTS } from '../nodes/Status200Uploads/shared/request';
import { description, locator, makeNode, nodeType, resolveParameters } from './support/fake';
import { packageFileExists } from './support/files.mjs';

function operations(): Array<{ resource: string; option: INodePropertyOptions }> {
	return description.properties
		.filter((p) => p.name === 'operation')
		.flatMap((p) =>
			(p.options as INodePropertyOptions[]).map((option) => ({
				resource: String(p.displayOptions?.show?.resource?.[0]),
				option,
			})),
		);
}

function issuesFor(user: Record<string, unknown>) {
	const parameters = resolveParameters(user);
	return NodeHelpers.getNodeParametersIssues(
		description.properties as INodeProperties[],
		makeNode(parameters),
		description,
	);
}

describe('the node', () => {
	it('is the declarative Status 200 Uploads node, usable as an AI tool', () => {
		expect(description).toMatchObject({
			name: 'status200Uploads',
			displayName: 'Status 200 Uploads',
			version: 1,
			usableAsTool: true,
			credentials: [{ name: CREDENTIAL_TYPE, required: true }],
		});
		expect(description.requestDefaults?.baseURL).toBe(API_BASE_URL);
		expect(description.requestDefaults?.headers).toMatchObject({ 'User-Agent': USER_AGENT });
		expect('execute' in nodeType).toBe(false);
	});

	it('has an operation for every endpoint it knows, each with the one preSend and postReceive', () => {
		const found = operations().map(({ resource, option }) => `${resource}.${String(option.value)}`);
		expect(found.sort()).toEqual(Object.keys(ENDPOINTS).sort());
		for (const { resource, option } of operations()) {
			const endpoint = ENDPOINTS[`${resource}.${String(option.value)}` as keyof typeof ENDPOINTS];
			expect(option.routing?.request).toMatchObject({
				method: endpoint.method,
				url: endpoint.path,
				ignoreHttpStatusErrors: true,
				returnFullResponse: true,
			});
			expect(option.routing?.send?.preSend).toEqual([prepareRequest]);
			expect(option.routing?.output?.postReceive).toEqual([handleAnswer]);
			expect(option.action, String(option.value)).toMatch(/^[A-Z][a-z]/);
		}
	});

	it('only operations carry routing: no parameter adds to the request behind preSend’s back', () => {
		const walk = (props: INodeProperties[]): string[] =>
			props.flatMap((p) => [
				...(p.routing ? [p.name] : []),
				...(p.type === 'collection' ? walk((p.options ?? []) as INodeProperties[]) : []),
			]);
		expect(walk(description.properties as INodeProperties[])).toEqual([]);
	});

	it('every list and dropdown method it names exists', () => {
		const listSearch = Object.keys(nodeType.methods.listSearch);
		const loadOptions = Object.keys(nodeType.methods.loadOptions);
		for (const p of description.properties) {
			for (const mode of p.modes ?? []) {
				const method = mode.typeOptions?.searchListMethod;
				if (method) expect(listSearch, p.name).toContain(method);
			}
			const load = p.typeOptions?.loadOptionsMethod;
			if (load) expect(loadOptions, p.name).toContain(load);
		}
	});

	it('its icons and codex file exist, and the codex names this package', () => {
		for (const icon of [description.icon, new Status200UploadsApi().icon]) {
			const { light, dark } = icon as { light: string; dark: string };
			for (const file of [light, dark]) expect(file).toMatch(/^file:/);
		}
		expect(packageFileExists('icons/status200uploads.svg')).toBe(true);
		expect(packageFileExists('icons/status200uploads.dark.svg')).toBe(true);
		expect(packageFileExists('nodes/Status200Uploads/Status200Uploads.node.json')).toBe(true);
	});
});

describe('parameters, as the n8n editor resolves them', () => {
	const account = locator('d4e5f6a7-b8c9-0123-def0-234567890123');

	it('a LinkedIn text post needs nothing more', () => {
		expect(
			issuesFor({
				resource: 'post',
				operation: 'create',
				account,
				platform: 'linkedin',
				text: 'Hi',
			}),
		).toBeNull();
	});

	it('TikTok asks for a privacy level, Pinterest for a board, Skool for a group and a title', () => {
		const tiktok = issuesFor({
			resource: 'post',
			operation: 'create',
			account,
			platform: 'tiktok',
		});
		expect(Object.keys(tiktok?.parameters ?? {})).toContain('tiktokPrivacyLevel');
		const pinterest = issuesFor({
			resource: 'post',
			operation: 'create',
			account,
			platform: 'pinterest',
		});
		expect(Object.keys(pinterest?.parameters ?? {})).toContain('pinterestBoardId');
		const skool = issuesFor({ resource: 'post', operation: 'create', account, platform: 'skool' });
		expect(Object.keys(skool?.parameters ?? {})).toEqual(
			expect.arrayContaining(['skoolGroup', 'skoolTitle']),
		);
	});

	it('At a Set Time asks for Scheduled For', () => {
		const issues = issuesFor({
			resource: 'post',
			operation: 'create',
			account,
			platform: 'x',
			text: 'Hi',
			when: 'later',
		});
		expect(Object.keys(issues?.parameters ?? {})).toContain('scheduledFor');
	});

	it('another network’s fields are dropped from the stored parameters', () => {
		const stored = resolveParameters({
			resource: 'post',
			operation: 'create',
			account,
			platform: 'x',
			tiktokPrivacyLevel: 'SELF_ONLY',
		});
		expect(stored).not.toHaveProperty('tiktokPrivacyLevel');
		expect(stored).toMatchObject({ platform: 'x', media: 'none', when: 'now' });
	});
});

describe('the credential', () => {
	const credential = new Status200UploadsApi();

	it('is one password field sent as a Bearer key', () => {
		expect(credential.name).toBe(CREDENTIAL_TYPE);
		expect(credential.properties).toHaveLength(1);
		expect(credential.properties[0]).toMatchObject({
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: true,
		});
		expect(credential.authenticate).toEqual({
			type: 'generic',
			properties: { headers: { Authorization: '=Bearer {{$credentials.apiKey}}' } },
		});
	});

	it('is tested with GET /api/v2/accounts', () => {
		expect(credential.test.request).toMatchObject({
			baseURL: API_BASE_URL,
			url: '/accounts',
			method: 'GET',
		});
		expect(credential.documentationUrl).toBe(
			'https://status200uploads.com/docs/api#authentication',
		);
	});
});
