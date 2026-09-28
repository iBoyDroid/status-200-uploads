import { NodeOperationError } from 'n8n-workflow';
import { describe, expect, it, vi } from 'vitest';
import {
	getPinterestBoards,
	getSkoolGroups,
	getTikTokPrivacyLevels,
	searchAccounts,
	searchPosts,
	searchScheduledPosts,
} from '../nodes/Status200Uploads/shared/methods';
import { FakeHttp, editorContext, json, locator } from './support/fake';

vi.mock('n8n-workflow', async (importOriginal) => ({
	...(await importOriginal<Record<string, unknown>>()),
	sleep: async () => undefined,
}));

const ID = 'd4e5f6a7-b8c9-0123-def0-234567890123';
const accounts = {
	data: [
		{ profile_id: ID, profile_name: 'MyShop', handle: '@MyShop', created_at: null, networks: [] },
		{
			profile_id: '11111111-b8c9-0123-def0-234567890123',
			profile_name: 'blog',
			handle: '@blog',
			created_at: null,
			networks: [],
		},
	],
};

function options(platform: string, row: Record<string, unknown>) {
	return json(200, {
		data: {
			profile_id: ID,
			profile_name: 'MyShop',
			networks: [
				{
					platform,
					status: 'ok',
					note: null,
					checked_at: null,
					cached: false,
					error_code: null,
					...row,
				},
			],
			note: null,
			asked_at: '2026-09-28T10:00:00Z',
		},
	});
}

describe('listSearch', () => {
	it('searchAccounts: "name (@handle)", the profile_id as value, filtered', async () => {
		const http = new FakeHttp().answer(json(200, accounts), json(200, accounts));
		const all = await searchAccounts.call(editorContext({}, http));
		expect(all.results).toEqual([
			{ name: 'MyShop (@MyShop)', value: ID },
			{ name: 'blog (@blog)', value: '11111111-b8c9-0123-def0-234567890123' },
		]);
		const some = await searchAccounts.call(editorContext({}, http), 'SHOP');
		expect(some.results.map((r) => r.value)).toEqual([ID]);
		expect(http.sent[0]).toMatchObject({ method: 'GET', url: '/accounts' });
	});

	it('searchPosts and searchScheduledPosts: newest first, the next page by cursor', async () => {
		const page = {
			data: [
				{
					id: 'p1',
					kind: 'post',
					platform: 'linkedin',
					status: 'success',
					at: '2026-09-28T10:00:00.000Z',
				},
				{
					id: 's1',
					kind: 'scheduled_post',
					platforms: ['tiktok', 'x'],
					status: 'scheduled',
					at: '2026-10-01T09:00:00.000Z',
				},
			],
			next_cursor: 'c1',
			next_url: 'u',
		};
		const http = new FakeHttp().answer(json(200, page), json(200, { ...page, next_cursor: null }));
		const first = await searchPosts.call(editorContext({}, http));
		expect(first).toEqual({
			results: [
				{ name: 'LinkedIn - success - 2026-09-28 10:00 UTC', value: 'p1' },
				{ name: 'TikTok, X - scheduled - 2026-10-01 09:00 UTC', value: 's1' },
			],
			paginationToken: 'c1',
		});
		const waiting = await searchScheduledPosts.call(editorContext({}, http), undefined, 'c1');
		expect(waiting.paginationToken).toBeUndefined();
		expect(http.sent[1].qs).toEqual({
			limit: 50,
			kind: 'scheduled_post',
			status: 'scheduled',
			cursor: 'c1',
		});
	});
});

describe('loadOptions from the chosen account', () => {
	it('TikTok privacy levels: only the ones this account allows', async () => {
		const http = new FakeHttp().answer(
			options('tiktok', {
				options: { privacy_level_options: ['SELF_ONLY', 'PUBLIC_TO_EVERYONE'] },
			}),
		);
		const levels = await getTikTokPrivacyLevels.call(
			editorContext(
				{ resource: 'post', operation: 'create', platform: 'tiktok', account: locator(ID) },
				http,
			),
		);
		expect(levels).toEqual([
			{ name: 'Only Me', value: 'SELF_ONLY' },
			{ name: 'Everyone', value: 'PUBLIC_TO_EVERYONE' },
		]);
		expect(http.sent[0]).toMatchObject({
			url: `/accounts/${ID}/options`,
			qs: { platforms: 'tiktok' },
		});
	});

	it('an @handle is looked up first', async () => {
		const http = new FakeHttp().answer(
			json(200, accounts),
			options('pinterest', {
				options: {
					boards: [
						{ id: '2', name: 'Recipes' },
						{ id: '1', name: 'Art' },
					],
				},
			}),
		);
		const boards = await getPinterestBoards.call(
			editorContext(
				{
					resource: 'post',
					operation: 'create',
					platform: 'pinterest',
					account: locator('@myshop', 'handle'),
				},
				http,
			),
		);
		expect(boards).toEqual([
			{ name: 'Art', value: '1' },
			{ name: 'Recipes', value: '2' },
		]);
		expect(http.sent[1].url).toBe(`/accounts/${ID}/options`);
	});

	it('Skool groups', async () => {
		const http = new FakeHttp().answer(
			options('skool', {
				options: { groups: [{ id: 'g1', slug: 'grp', name: 'Group' }], labels: null },
			}),
		);
		const groups = await getSkoolGroups.call(
			editorContext(
				{ resource: 'post', operation: 'create', platform: 'skool', account: locator(ID) },
				http,
			),
		);
		expect(groups).toEqual([{ name: 'Group', value: 'g1' }]);
	});

	it('says what to do when there is no account, or the network cannot give choices', async () => {
		const none = getTikTokPrivacyLevels.call(
			editorContext({ resource: 'post', operation: 'create', platform: 'tiktok' }, new FakeHttp()),
		);
		await expect(none).rejects.toThrow('Choose an account first');
		const http = new FakeHttp().answer(
			options('tiktok', {
				status: 'reconnect_required',
				options: null,
				note: 'Reconnect TikTok on the Connections page.',
			}),
		);
		const error = await getTikTokPrivacyLevels
			.call(
				editorContext(
					{ resource: 'post', operation: 'create', platform: 'tiktok', account: locator(ID) },
					http,
				),
			)
			.catch((e: unknown) => e);
		expect(error).toBeInstanceOf(NodeOperationError);
		expect((error as NodeOperationError).description).toBe(
			'Reconnect TikTok on the Connections page.',
		);
	});
});
