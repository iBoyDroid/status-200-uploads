// The workflow templates in templates/ (what n8n's Creator Portal gets, and what the README points to).
// They follow n8n's template rules and carry no credentials. Run through n8n's own expression engine,
// with the OpenAPI file's example answers standing in for the API, their Status 200 Uploads nodes send
// the requests they should:
//   - T1 cross-posts one image and one text to X, LinkedIn and Facebook, then reads each post back;
//   - T2 imports one video for TikTok, Instagram Reels and YouTube Shorts and either only checks it (a
//     dry run), schedules it (to be stopped with Post: Cancel), or posts it and reads it until done.

import {
	createRunExecutionData,
	NodeHelpers,
	Workflow,
	type IConnections,
	type IDataObject,
	type IHttpRequestOptions,
	type INode,
	type INodeExecutionData,
	type INodeProperties,
	type INodeTypes,
	type ITaskData,
	type NodeParameterValueType,
} from 'n8n-workflow';
import { describe, expect, it } from 'vitest';
import { MAX_WAIT_LIMIT_SECONDS } from '../nodes/Status200Uploads/shared/constants';
import {
	description,
	FakeHttp,
	itemContext,
	json,
	locator,
	makeNode,
	resolveParameters,
	runItem,
	type Scripted,
} from './support/fake';
import { listPackageFiles, readPackageFile } from './support/files.mjs';
import { check, responseExamples, spec } from './support/spec';

const NODE_TYPE = '@status200uploads/n8n-nodes-status200uploads.status200Uploads';
const PROFILE_ID = 'd4e5f6a7-b8c9-0123-def0-234567890123';
const KEY = /^n8n-[0-9a-f]{64}$/;

const T1 = 'templates/cross-post-x-linkedin-facebook.json';
const T2 = 'templates/short-video-tiktok-instagram-youtube.json';

/** The node types a template may use, at the versions n8n 2.40 ships (n8n-nodes-base 2.40.2). */
const STANDARD_NODES: Record<string, number> = {
	'n8n-nodes-base.manualTrigger': 1,
	'n8n-nodes-base.set': 3.4,
	'n8n-nodes-base.merge': 3.2,
	'n8n-nodes-base.if': 2.2,
	'n8n-nodes-base.wait': 1.1,
	'n8n-nodes-base.stickyNote': 1,
};
const STICKY = 'n8n-nodes-base.stickyNote';

/** n8n's default node names, which the template rules say to replace. */
const DEFAULT_NAMES = [
	'Status 200 Uploads',
	'When clicking ‘Execute workflow’',
	'Edit Fields',
	'Merge',
	'If',
	'Wait',
	'Sticky Note',
	'Schedule Trigger',
];

/** What the reader must still choose in each Status 200 Uploads node after importing. */
const LEFT_TO_CHOOSE: Record<string, string[]> = {
	'Publish to X': ['account'],
	'Publish to LinkedIn': ['account'],
	'Publish to Facebook': ['account'],
	'Publish to TikTok': ['account', 'tiktokPrivacyLevel'],
	'Publish to Instagram Reels': ['account'],
	'Publish to YouTube Shorts': ['account'],
};

interface Template {
	name: string;
	nodes: INode[];
	connections: IConnections;
	pinData?: IDataObject;
	settings?: IDataObject;
}

interface Assignment {
	name: string;
	value: unknown;
	type: string;
}

const FILES = listPackageFiles('templates').filter((f) => f.endsWith('.json'));

function load(file: string): Template {
	return JSON.parse(readPackageFile(file)) as Template;
}

function words(text: string): number {
	return text.split(/\s+/).filter((w) => w !== '').length;
}

function nodeNamed(t: Template, name: string): INode {
	const node = t.nodes.find((n) => n.name === name);
	if (!node) throw new Error(`no node "${name}"`);
	return node;
}

/** Every [source, target] connection of a template. */
function edges(t: Template): Array<[string, string]> {
	const out: Array<[string, string]> = [];
	for (const [source, byType] of Object.entries(t.connections)) {
		for (const outputs of Object.values(byType)) {
			for (const output of outputs ?? []) {
				for (const target of output ?? []) out.push([source, target.node]);
			}
		}
	}
	return out;
}

/** The nodes a node can be reached from. */
function upstreamOf(t: Template, name: string): Set<string> {
	const seen = new Set<string>();
	const walk = (target: string) => {
		for (const [source, to] of edges(t)) {
			if (to === target && !seen.has(source)) {
				seen.add(source);
				walk(source);
			}
		}
	};
	walk(name);
	return seen;
}

function assignmentsOf(node: INode): Assignment[] {
	return ((node.parameters.assignments as IDataObject).assignments ?? []) as Assignment[];
}

describe('the templates', () => {
	it('are the two templates of the plan', () => {
		expect(FILES).toEqual([T1, T2]);
	});

	for (const file of FILES) {
		describe(file, () => {
			const t = load(file);
			const text = readPackageFile(file);
			const stickies = t.nodes.filter((n) => n.type === STICKY);
			const working = t.nodes.filter((n) => n.type !== STICKY);
			const ours = t.nodes.filter((n) => n.type === NODE_TYPE);

			it('is a plain workflow: no credentials, ids of an instance, pinned data or personal details', () => {
				expect(Object.keys(t).sort()).toEqual([
					'connections',
					'name',
					'nodes',
					'pinData',
					'settings',
				]);
				expect(t.pinData).toEqual({});
				expect(t.settings).toEqual({ executionOrder: 'v1' });
				for (const node of t.nodes) expect(node.credentials, node.name).toBeUndefined();
				expect(text).not.toMatch(/rl_[0-9A-Za-z]{8,}|instanceId|credentials|[\w.+-]+@[\w-]+\.\w+/);
				expect(text).not.toMatch(/\r/);
			});

			it('has a sentence-case title with no emoji', () => {
				expect(t.name).toMatch(/^[A-Z][^A-Z]/);
				expect(t.name).not.toMatch(/\p{Extended_Pictographic}/u);
			});

			it('uses only its own node and the n8n core nodes of n8n 2.40', () => {
				for (const node of t.nodes) {
					if (node.type === NODE_TYPE) expect(node.typeVersion, node.name).toBe(1);
					else
						expect(node.typeVersion, `${node.name} (${node.type})`).toBe(STANDARD_NODES[node.type]);
				}
			});

			it('names every node, once, and none by n8n’s default name', () => {
				const names = t.nodes.map((n) => n.name);
				expect(new Set(names).size).toBe(names.length);
				for (const name of names) {
					expect(DEFAULT_NAMES, name).not.toContain(name);
					expect(name, 'an n8n copy suffix').not.toMatch(/\d$/);
				}
				const ids = t.nodes.map((n) => n.id);
				expect(new Set(ids).size).toBe(ids.length);
			});

			it('connects every working node, from one manual trigger, to nodes that exist', () => {
				const names = new Set(t.nodes.map((n) => n.name));
				const triggers = working.filter((n) => n.type === 'n8n-nodes-base.manualTrigger');
				expect(triggers).toHaveLength(1);
				for (const [source, target] of edges(t)) {
					expect(names.has(source), source).toBe(true);
					expect(names.has(target), target).toBe(true);
				}
				const targets = new Set(edges(t).map(([, to]) => to));
				for (const node of working) {
					if (node === triggers[0]) continue;
					expect(targets.has(node.name), `${node.name} has no input`).toBe(true);
				}
			});

			it('has one overview sticky (How it works, Setup, 100 to 300 words) and short section stickies', () => {
				const overview = stickies.filter((n) =>
					[undefined, 1].includes(n.parameters.color as number),
				);
				expect(overview).toHaveLength(1);
				const content = String(overview[0].parameters.content);
				expect(content).toContain('### How it works');
				expect(content).toContain('### Setup');
				expect(words(content)).toBeGreaterThanOrEqual(100);
				expect(words(content)).toBeLessThanOrEqual(300);
				expect(content).toContain('@status200uploads/n8n-nodes-status200uploads');
				expect(content).toMatch(/self-hosted/);
				const sections = stickies.filter((n) => n !== overview[0]);
				expect(sections.length).toBeGreaterThan(0);
				for (const note of sections) {
					expect(note.parameters.color, note.name).toBe(7);
					expect(words(String(note.parameters.content)), note.name).toBeLessThan(50);
				}
			});

			it('keeps what the reader sets in one Set node, "Your settings", and refers only to its fields', () => {
				const settings = nodeNamed(t, 'Your settings');
				expect(settings.type).toBe('n8n-nodes-base.set');
				const fields = assignmentsOf(settings).map((a) => a.name);
				for (const m of text.matchAll(/\$\('Your settings'\)\.item\.json\.(\w+)/g))
					expect(fields, m[0]).toContain(m[1]);
			});

			it('refers in expressions only to nodes that run before', () => {
				for (const node of working) {
					const upstream = upstreamOf(t, node.name);
					for (const m of JSON.stringify(node.parameters).matchAll(/\$\('([^']+)'\)/g))
						expect(upstream.has(m[1]), `${node.name} reads ${m[1]}`).toBe(true);
				}
			});

			it('its Status 200 Uploads nodes resolve, missing only what the reader chooses', () => {
				expect(ours.length).toBeGreaterThan(0);
				for (const node of ours) {
					const parameters = resolveParameters(node.parameters);
					const issues = NodeHelpers.getNodeParametersIssues(
						description.properties as INodeProperties[],
						makeNode(parameters),
						description,
					);
					expect(Object.keys(issues?.parameters ?? {}).sort(), node.name).toEqual(
						LEFT_TO_CHOOSE[node.name] ?? [],
					);
				}
			});

			it('posts and imports with the automatic Idempotency-Key, and waits within the node’s limit', () => {
				for (const node of ours) {
					const options = (node.parameters.options ?? {}) as IDataObject;
					expect(options.idempotencyKeyMode, node.name).toBeUndefined();
					expect(options.customIdempotencyKey, node.name).toBeUndefined();
					if (options.maxWait !== undefined)
						expect(Number(options.maxWait)).toBeLessThanOrEqual(MAX_WAIT_LIMIT_SECONDS);
				}
			});
		});
	}
});

// ---------------------------------------------------------------------------------------------------
// Running the templates: n8n's expression engine over recorded outputs, and the node over scripted
// answers taken from the OpenAPI file.

const STUB_TYPE = {
	description: { properties: [], inputs: ['main'], outputs: ['main'], version: 1, defaults: {} },
};
const STUB_TYPES = {
	getByName: () => STUB_TYPE,
	getByNameAndVersion: () => STUB_TYPE,
	getKnownTypes: () => ({}),
} as unknown as INodeTypes;

function item(data: IDataObject, index = 0): INodeExecutionData {
	return { json: data, pairedItem: { item: index } };
}

/** One run of a template: what each node output so far, and n8n's expressions over it. */
class TemplateRun {
	readonly template: Template;
	private readonly workflow: Workflow;
	private readonly runData: Record<string, ITaskData[]> = {};

	constructor(file: string) {
		this.template = load(file);
		// The Workflow gets a copy: it resolves the copy's parameters against the stub types.
		this.workflow = new Workflow({
			id: 'wf-template',
			name: this.template.name,
			nodes: JSON.parse(JSON.stringify(this.template.nodes)) as INode[],
			connections: this.template.connections,
			active: false,
			nodeTypes: STUB_TYPES,
			settings: this.template.settings,
		});
	}

	node(name: string): INode {
		return nodeNamed(this.template, name);
	}

	/** Records one run of a node: its output items, and the node its input came from. */
	output(name: string, items: INodeExecutionData[], from: string | null): INodeExecutionData[] {
		const task: ITaskData = {
			startTime: 0,
			executionTime: 0,
			executionIndex: 0,
			source: from ? [{ previousNode: from }] : [],
			data: { main: [items] },
		};
		(this.runData[name] ??= []).push(task);
		return items;
	}

	/** A parameter value of a node for one item of its input, resolved as n8n resolves it. */
	resolve(
		name: string,
		value: unknown,
		input: INodeExecutionData[],
		from: string,
		itemIndex: number,
		runIndex = 0,
	): unknown {
		const node = this.node(name);
		return this.workflow.expression.getParameterValue(
			value as NodeParameterValueType,
			createRunExecutionData({ resultData: { runData: this.runData } }),
			runIndex,
			itemIndex,
			name,
			input,
			'manual',
			{},
			{ node, data: { main: [input] }, source: { main: [{ previousNode: from }] } },
		);
	}

	/** The output of "Your settings", with the reader's changes. */
	settings(changes: IDataObject = {}): INodeExecutionData[] {
		this.output('Run by hand', [item({})], null);
		const values = Object.fromEntries(
			assignmentsOf(this.node('Your settings')).map((a) => [a.name, a.value]),
		) as IDataObject;
		return this.output('Your settings', [item({ ...values, ...changes })], 'Run by hand');
	}

	/**
	 * A Status 200 Uploads node over its input: each item's parameters resolved by n8n, the reader's
	 * choices added (the account, and whatever else `choose` names), then the node's own preSend and
	 * postReceive with the scripted answers.
	 */
	async ours(
		name: string,
		input: INodeExecutionData[],
		from: string,
		answers: Scripted[],
		options: { choose?: IDataObject; timezone?: string; runIndex?: number } = {},
	): Promise<{ sent: IHttpRequestOptions[]; out: INodeExecutionData[] }> {
		const node = this.node(name);
		const http = new FakeHttp().answer(...answers);
		const out: INodeExecutionData[] = [];
		for (let i = 0; i < input.length; i++) {
			const resolved = this.resolve(
				name,
				node.parameters,
				input,
				from,
				i,
				options.runIndex,
			) as IDataObject;
			const user: IDataObject = { ...resolved, ...options.choose };
			if (resolved.account) user.account = locator(PROFILE_ID);
			const ctx = itemContext(user, http, {
				itemIndex: i,
				timezone: options.timezone ?? 'UTC',
				workflowId: 'wf-template',
				executionId: 'exec-template',
			});
			out.push(...(await runItem(ctx, http)));
		}
		expect(http.left, `${name}: answers left over`).toBe(0);
		return { sent: http.sent, out: this.output(name, out, from) };
	}

	/** What an IF node's one condition gives for each item. */
	condition(name: string, input: INodeExecutionData[], from: string, runIndex = 0): boolean[] {
		const conditions = (this.node(name).parameters.conditions as IDataObject).conditions as Array<{
			leftValue: string;
			operator: { type: string; operation: string };
		}>;
		expect(conditions).toHaveLength(1);
		expect(conditions[0].operator).toMatchObject({ type: 'boolean', operation: 'true' });
		return input.map(
			(_, i) => this.resolve(name, conditions[0].leftValue, input, from, i, runIndex) as boolean,
		);
	}

	/** What a Set node outputs for each item. */
	fields(name: string, input: INodeExecutionData[], from: string): IDataObject[] {
		const list = assignmentsOf(this.node(name));
		return input.map(
			(_, i) =>
				Object.fromEntries(
					list.map((a) => [a.name, this.resolve(name, a.value, input, from, i)]),
				) as IDataObject,
		);
	}
}

/** Merge (append): the items of every input, in input order. */
function merged(...outputs: INodeExecutionData[][]): INodeExecutionData[] {
	return outputs.flat().map((entry, index) => ({ ...entry, pairedItem: { item: index } }));
}

const published = responseExamples('Published') as Record<string, IDataObject>;
const accepted = responseExamples('Accepted') as Record<string, IDataObject>;
const mediaReady = (spec.components.schemas.MediaImportReady as IDataObject).example as IDataObject;

function withPostId(answer: IDataObject, postId: string): IDataObject {
	return {
		...answer,
		status200: {
			...(answer.status200 as IDataObject),
			post_id: postId,
			status_url: `https://status200uploads.com/api/v2/posts/${postId}`,
		},
	};
}

/** GET /posts/{id} of a post, checked against the file's PostRead schema. */
function postRead(
	id: string,
	platform: string,
	status: string,
	done: boolean,
	permalink: string | null,
): Scripted {
	const body = {
		data: {
			id,
			kind: 'post',
			profile_id: PROFILE_ID,
			platform,
			status,
			done,
			media_type: 'image',
			publish_id: null,
			permalink,
			error_message: null,
			at: '2026-09-28T10:00:00.000Z',
			updated_at: '2026-09-28T10:00:05.000Z',
			scheduled_post_id: null,
			figures: null,
		},
	};
	expect(check('/components/schemas/PostRead', body)).toBe('');
	return json(200, body);
}

function importAnswer(type: string): Scripted {
	const body = { ...mediaReady, type };
	expect(check('/components/schemas/MediaImportReady', body)).toBe('');
	return json(200, body);
}

function keyOf(sent: IHttpRequestOptions): string | undefined {
	return (sent.headers as Record<string, string> | undefined)?.['Idempotency-Key'];
}

describe('T1 run: cross-post an image to X, LinkedIn and Facebook', () => {
	async function runT1(changes: IDataObject = {}) {
		const run = new TemplateRun(T1);
		const settings = run.settings(changes);
		const imported = await run.ours('Import image', settings, 'Your settings', [
			importAnswer('image/jpeg'),
		]);
		const ids = {
			x: 'e5f6a7b8-c9d0-4234-8f01-345678901234',
			linkedin: 'f6a7b8c9-d0e1-4345-9012-456789012345',
			facebook: 'a7b8c9d0-e1f2-4456-a123-567890123456',
		};
		const x = await run.ours('Publish to X', imported.out, 'Import image', [
			json(200, withPostId(published.x, ids.x)),
		]);
		const linkedin = await run.ours('Publish to LinkedIn', imported.out, 'Import image', [
			json(200, withPostId(published.linkedin, ids.linkedin)),
		]);
		const facebook = await run.ours('Publish to Facebook', imported.out, 'Import image', [
			json(200, withPostId(published.facebook, ids.facebook)),
		]);
		const answers = run.output(
			'Collect the answers',
			merged(x.out, linkedin.out, facebook.out),
			'Publish to X',
		);
		const read = await run.ours('Read each post', answers, 'Collect the answers', [
			postRead(ids.x, 'x', 'success', true, 'https://x.com/i/status/1841234567890123456'),
			postRead(
				ids.linkedin,
				'linkedin',
				'success',
				true,
				'https://www.linkedin.com/feed/update/urn:li:share:1',
			),
			postRead(ids.facebook, 'facebook', 'success', true, 'https://www.facebook.com/1/posts/2'),
		]);
		const summary = run.fields('Summary', read.out, 'Read each post');
		return { settings: settings[0].json, imported, x, linkedin, facebook, read, summary, ids };
	}

	it('imports the image once, with a key, and posts its file_id with the text to each network', async () => {
		const r = await runT1();
		expect(r.imported.sent).toHaveLength(1);
		expect(r.imported.sent[0]).toMatchObject({
			method: 'POST',
			url: '/media',
			body: { url: 'https://example.com/autumn-guide.jpg' },
		});
		expect(keyOf(r.imported.sent[0])).toMatch(KEY);
		const content = { text: r.settings.post_text, mediaID: [mediaReady.file_id] };
		for (const [step, platform] of [
			[r.x, 'x'],
			[r.linkedin, 'linkedin'],
			[r.facebook, 'facebook'],
		] as const) {
			expect(step.sent).toHaveLength(1);
			expect(step.sent[0]).toMatchObject({ method: 'POST', url: '/posts' });
			expect(step.sent[0].body).toEqual({ post: { accountId: PROFILE_ID, platform, content } });
			expect(keyOf(step.sent[0])).toMatch(KEY);
		}
		const keys = [r.x, r.linkedin, r.facebook].map((s) => keyOf(s.sent[0]));
		expect(new Set(keys).size).toBe(3);
	});

	it('sends x_text to X only, when it is filled in', async () => {
		const r = await runT1({ x_text: 'Short for X' });
		expect(r.x.sent[0].body).toMatchObject({ post: { platform: 'x', x: { text: 'Short for X' } } });
		expect((r.linkedin.sent[0].body as IDataObject).post).not.toHaveProperty('linkedin');
	});

	it('reads each post back by its status200.post_id and sums up network, status and link', async () => {
		const r = await runT1();
		expect(r.read.sent.map((s) => `${String(s.method)} ${String(s.url)}`)).toEqual([
			`GET /posts/${r.ids.x}`,
			`GET /posts/${r.ids.linkedin}`,
			`GET /posts/${r.ids.facebook}`,
		]);
		expect(r.summary).toEqual([
			{
				network: 'x',
				status: 'success',
				link: 'https://x.com/i/status/1841234567890123456',
				problem: '',
				post_id: r.ids.x,
			},
			{
				network: 'linkedin',
				status: 'success',
				link: 'https://www.linkedin.com/feed/update/urn:li:share:1',
				problem: '',
				post_id: r.ids.linkedin,
			},
			{
				network: 'facebook',
				status: 'success',
				link: 'https://www.facebook.com/1/posts/2',
				problem: '',
				post_id: r.ids.facebook,
			},
		]);
	});

	it('reads a post queued for the next day by its scheduled_post_id', async () => {
		const run = new TemplateRun(T1);
		const queued = accepted.queued;
		const input = [item(queued)];
		run.output('Collect the answers', input, 'Publish to X');
		const read = await run.ours('Read each post', input, 'Collect the answers', [
			json(200, {
				data: {
					id: (queued.status200 as IDataObject).scheduled_post_id,
					kind: 'scheduled_post',
					profile_id: PROFILE_ID,
					platforms: ['x'],
					status: 'scheduled',
					outcome: 'waiting',
					done: false,
					media_type: 'image',
					at: '2026-09-29T14:30:00.000Z',
					scheduled_for: '2026-09-29T14:30:00.000Z',
					created_at: '2026-09-28T14:30:00.000Z',
					updated_at: '2026-09-28T14:30:00.000Z',
					note: 'Daily post limit reached',
					error_message: null,
					results: [],
				},
			}),
		]);
		expect(read.sent[0].url).toBe(
			`/posts/${String((queued.status200 as IDataObject).scheduled_post_id)}`,
		);
		expect(run.fields('Summary', read.out, 'Read each post')[0]).toMatchObject({
			network: 'x',
			status: 'scheduled',
			link: '',
		});
	});
});

describe('T2 run: a short video to TikTok, Instagram Reels and YouTube Shorts', () => {
	const PUBLISH = ['Publish to TikTok', 'Publish to Instagram Reels', 'Publish to YouTube Shorts'];
	const PLATFORMS = ['tiktok', 'instagram', 'youtube'];
	const CHOOSE: Record<string, IDataObject> = {
		'Publish to TikTok': { tiktokPrivacyLevel: 'SELF_ONLY' },
	};

	/** Settings, the import and the three posts, each answered by `answer(platform)`. */
	async function publish(
		changes: IDataObject,
		answer: (platform: string, index: number) => Scripted,
		timezone = 'UTC',
	) {
		const run = new TemplateRun(T2);
		const settings = run.settings(changes);
		const imported = await run.ours('Import video', settings, 'Your settings', [
			importAnswer('video/mp4'),
		]);
		const steps = [];
		for (const [index, name] of PUBLISH.entries()) {
			steps.push(
				await run.ours(name, imported.out, 'Import video', [answer(PLATFORMS[index], index)], {
					choose: CHOOSE[name],
					timezone,
				}),
			);
		}
		const answers = run.output(
			'Collect the answers',
			merged(...steps.map((s) => s.out)),
			PUBLISH[0],
		);
		return { run, settings: settings[0].json, imported, steps, answers };
	}

	function networkBlocks(settings: IDataObject): IDataObject[] {
		return [
			{ tiktok: { privacyLevel: 'SELF_ONLY' } },
			{ instagram: { postType: 'reel' } },
			{ youtube: { privacyStatus: 'private', title: settings.youtube_title } },
		];
	}

	it('as shipped (check_only true) only checks: dryRun, no key, nothing scheduled, a report per network', async () => {
		const r = await publish({}, (platform) =>
			json(200, {
				...published.dryRun,
				target: { ...(published.dryRun.target as IDataObject), platform },
			}),
		);
		expect(r.settings.check_only).toBe(true);
		expect(r.imported.sent[0]).toMatchObject({
			method: 'POST',
			url: '/media',
			body: { url: 'https://example.com/short-video.mp4' },
		});
		const blocks = networkBlocks(r.settings);
		for (const [index, step] of r.steps.entries()) {
			expect(step.sent[0].body).toEqual({
				post: {
					accountId: PROFILE_ID,
					platform: PLATFORMS[index],
					content: { text: r.settings.caption, mediaID: [mediaReady.file_id] },
					...blocks[index],
				},
				dryRun: true,
			});
			expect(keyOf(step.sent[0])).toBeUndefined();
		}
		expect(r.run.condition('Sent now?', r.answers, 'Collect the answers')).toEqual([
			false,
			false,
			false,
		]);
		expect(r.run.fields('Checks and schedules', r.answers, 'Sent now?')).toEqual(
			PLATFORMS.map((network) => ({
				network,
				result: 'checked: publish',
				scheduled_post_id: '',
				scheduled_at: '',
			})),
		);
	});

	it('a refused check reports the reason', async () => {
		const r = await publish({}, (platform) =>
			json(200, {
				...published.dryRun,
				target: { ...(published.dryRun.target as IDataObject), platform },
				outcome: 'refuse',
				would_publish: false,
				reason: { code: 'reconnect_required', message: 'Reconnect TikTok.', status: 401 },
			}),
		);
		expect(r.run.fields('Checks and schedules', r.answers, 'Sent now?')[0]).toMatchObject({
			network: 'tiktok',
			result: 'checked: refuse (reconnect_required: Reconnect TikTok.)',
		});
	});

	it('with publish_at, schedules it in the workflow’s time zone; the report names the scheduled post to cancel', async () => {
		const r = await publish(
			{ check_only: false, publish_at: '2026-10-01 09:00' },
			(platform, index) => {
				const id = `c3d4e5f6-a7b8-4012-8def-12345678901${index}`;
				return json(202, {
					...accepted.scheduled,
					platform,
					scheduled_post_id: id,
					status200: {
						post_id: null,
						scheduled_post_id: id,
						status_url: `https://status200uploads.com/api/v2/posts/${id}`,
					},
				});
			},
			'Europe/Berlin',
		);
		for (const step of r.steps) {
			expect(step.sent[0].body).toMatchObject({
				post: { scheduledFor: '2026-10-01T07:00:00.000Z' },
			});
			expect(step.sent[0].body).not.toHaveProperty('dryRun');
			expect(keyOf(step.sent[0])).toMatch(KEY);
		}
		expect(r.run.condition('Sent now?', r.answers, 'Collect the answers')).toEqual([
			false,
			false,
			false,
		]);
		expect(r.run.fields('Checks and schedules', r.answers, 'Sent now?')).toEqual(
			PLATFORMS.map((network, index) => ({
				network,
				result: 'scheduled',
				scheduled_post_id: `c3d4e5f6-a7b8-4012-8def-12345678901${index}`,
				scheduled_at: '2026-10-01T09:00:00.000Z',
			})),
		);
	});

	it('posting now, reads each post every pass until it is done, then reports it', async () => {
		const ids = [
			'b2c3d4e5-f6a7-4901-8cde-f12345678901',
			'b2c3d4e5-f6a7-4901-8cde-f12345678902',
			'b2c3d4e5-f6a7-4901-8cde-f12345678903',
		];
		const r = await publish({ check_only: false }, (platform, index) =>
			platform === 'youtube'
				? json(202, withPostId(accepted.processing, ids[index]))
				: json(200, withPostId(published[platform], ids[index])),
		);
		for (const step of r.steps) {
			expect(step.sent[0].body).not.toHaveProperty('dryRun');
			expect(step.sent[0].body).not.toHaveProperty(['post', 'scheduledFor']);
			expect(keyOf(step.sent[0])).toMatch(KEY);
		}
		expect(r.run.condition('Sent now?', r.answers, 'Collect the answers')).toEqual([
			true,
			true,
			true,
		]);

		// First pass: straight from "Sent now?", by status200.post_id.
		const first = await r.run.ours(
			'Read the post',
			r.answers,
			'Sent now?',
			ids.map((id, i) => postRead(id, PLATFORMS[i], 'processing', false, null)),
		);
		expect(first.sent.map((s) => s.url)).toEqual(ids.map((id) => `/posts/${id}`));
		expect(r.run.condition('Live yet?', first.out, 'Read the post', 0)).toEqual([
			false,
			false,
			false,
		]);
		expect(r.run.condition('Live yet?', first.out, 'Read the post', 20)).toEqual([
			true,
			true,
			true,
		]);

		// Next pass: back from "Wait 30 seconds", with Read the post's own output, by its id.
		r.run.output('Wait 30 seconds', first.out, 'Live yet?');
		const links = [
			'https://www.tiktok.com/@me/video/1',
			'https://www.instagram.com/reel/2',
			'https://youtube.com/shorts/3',
		];
		const second = await r.run.ours(
			'Read the post',
			first.out,
			'Wait 30 seconds',
			ids.map((id, i) => postRead(id, PLATFORMS[i], 'success', true, links[i])),
			{ runIndex: 1 },
		);
		expect(second.sent.map((s) => s.url)).toEqual(ids.map((id) => `/posts/${id}`));
		expect(r.run.condition('Live yet?', second.out, 'Read the post', 1)).toEqual([
			true,
			true,
			true,
		]);
		expect(r.run.fields('Report', second.out, 'Live yet?')).toEqual(
			PLATFORMS.map((network, i) => ({
				network,
				status: 'success',
				done: true,
				link: links[i],
				problem: '',
			})),
		);
	});
});
