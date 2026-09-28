import {
	NodeOperationError,
	type IDataObject,
	type ILoadOptionsFunctions,
	type INodeListSearchItems,
	type INodeListSearchResult,
	type INodePropertyOptions,
} from 'n8n-workflow';
import { EDITOR_MAX_WAIT_SECONDS, PLATFORM_NAMES, UUID_PATTERN, type Platform } from './constants';
import { dataList, dataObject } from './output';
import type { ApiRequest, Operation } from './request';
import { call, type Policy } from './transport';

const EDITOR_POLICY: Policy = {
	kind: 'read',
	waitWhenAsked: true,
	maxWaitSeconds: EDITOR_MAX_WAIT_SECONDS,
};
const UUID = new RegExp(`^${UUID_PATTERN}$`);

function readRequest(operation: Operation, url: string, qs: IDataObject = {}): ApiRequest {
	return { operation, method: 'GET', url, qs, headers: {}, keySent: false, repeatable: true };
}

function text(value: unknown): string {
	return typeof value === 'string' ? value : typeof value === 'number' ? String(value) : '';
}

function matches(filter: string | undefined, ...fields: string[]): boolean {
	const f = (filter ?? '').trim().toLowerCase();
	return f === '' || fields.some((field) => field.toLowerCase().includes(f));
}

async function accounts(this: ILoadOptionsFunctions): Promise<IDataObject[]> {
	const answer = await call(this, readRequest('account.getAll', '/accounts'), EDITOR_POLICY);
	return dataList(answer.body);
}

/** Account list: "name (@handle)", the value is the profile_id. */
export async function searchAccounts(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const results: INodeListSearchItems[] = (await accounts.call(this))
		.filter((a) => matches(filter, text(a.profile_name), text(a.handle)))
		.map((a) => ({
			name: `${text(a.profile_name)} (${text(a.handle)})`,
			value: text(a.profile_id),
		}));
	return { results };
}

function postName(item: IDataObject): string {
	const platforms = Array.isArray(item.platforms)
		? item.platforms.map(String)
		: [text(item.platform)];
	const names = platforms.map((p) => PLATFORM_NAMES[p as Platform] ?? p).join(', ');
	const when = text(item.at).replace('T', ' ').slice(0, 16);
	return [names, text(item.status), when ? `${when} UTC` : '']
		.filter((part) => part !== '')
		.join(' - ');
}

async function searchPostList(
	this: ILoadOptionsFunctions,
	qs: IDataObject,
	filter?: string,
	cursor?: string,
): Promise<INodeListSearchResult> {
	const answer = await call(
		this,
		readRequest('post.getAll', '/posts', { limit: 50, ...qs, ...(cursor ? { cursor } : {}) }),
		EDITOR_POLICY,
	);
	const results: INodeListSearchItems[] = dataList(answer.body)
		.map((item) => ({ name: postName(item), value: text(item.id) }))
		.filter((item) => matches(filter, item.name, item.value));
	const next = text(answer.body?.next_cursor);
	return next ? { results, paginationToken: next } : { results };
}

/** Recent posts and scheduled posts, newest first. */
export async function searchPosts(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	return await searchPostList.call(this, {}, filter, paginationToken);
}

/** Posts that are still waiting to go out (the ones Post: Cancel can stop). */
export async function searchScheduledPosts(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	return await searchPostList.call(
		this,
		{ kind: 'scheduled_post', status: 'scheduled' },
		filter,
		paginationToken,
	);
}

/** The profile_id of the chosen account; an @handle is looked up in GET /accounts. */
async function chosenProfileId(this: ILoadOptionsFunctions): Promise<string> {
	const value = text(this.getCurrentNodeParameter('account', { extractValue: true })).trim();
	if (value === '') {
		throw new NodeOperationError(this.getNode(), 'Choose an account first', {
			description: 'This list comes from the account: choose it above, then open this list again',
		});
	}
	if (UUID.test(value)) return value.toLowerCase();
	const name = value.replace(/^@/, '').toLowerCase();
	const found = (await accounts.call(this)).filter(
		(a) =>
			text(a.profile_name).toLowerCase() === name || text(a.handle).toLowerCase() === `@${name}`,
	);
	if (found.length !== 1) {
		throw new NodeOperationError(
			this.getNode(),
			`No single profile named ${value} on your account`,
			{
				description: 'Choose the account from the list, or give its ID',
			},
		);
	}
	return text(found[0].profile_id);
}

/** One network's row of GET /accounts/{profile_id}/options, when it can post. */
async function networkOptions(
	this: ILoadOptionsFunctions,
	platform: Platform,
): Promise<IDataObject> {
	const profileId = await chosenProfileId.call(this);
	const answer = await call(
		this,
		readRequest('account.getPostingOptions', `/accounts/${profileId}/options`, {
			platforms: platform,
		}),
		EDITOR_POLICY,
	);
	const networks = dataObject(answer.body).networks;
	const row = Array.isArray(networks)
		? (networks as IDataObject[]).find((n) => n.platform === platform)
		: undefined;
	const options = row?.options;
	if (!row || row.status !== 'ok' || typeof options !== 'object' || options === null) {
		throw new NodeOperationError(
			this.getNode(),
			`${PLATFORM_NAMES[platform]} gave no choices for this account`,
			{
				description:
					text(row?.note) ||
					`Check that ${PLATFORM_NAMES[platform]} is connected for this profile on the Connections page`,
			},
		);
	}
	return options as IDataObject;
}

const PRIVACY_NAMES: Record<string, string> = {
	PUBLIC_TO_EVERYONE: 'Everyone',
	MUTUAL_FOLLOW_FRIENDS: 'Friends (Mutual Followers)',
	FOLLOWER_OF_CREATOR: 'Followers',
	SELF_ONLY: 'Only Me',
};

/** The privacy levels TikTok accepts for this account right now. */
export async function getTikTokPrivacyLevels(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const options = await networkOptions.call(this, 'tiktok');
	const levels = Array.isArray(options.privacy_level_options)
		? options.privacy_level_options.map(String)
		: [];
	return levels.map((level) => ({ name: PRIVACY_NAMES[level] ?? level, value: level }));
}

/** The account's Pinterest boards. */
export async function getPinterestBoards(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const options = await networkOptions.call(this, 'pinterest');
	const boards = Array.isArray(options.boards) ? (options.boards as IDataObject[]) : [];
	return boards
		.filter((b) => text(b.id) !== '')
		.map((b) => ({ name: text(b.name) || text(b.id), value: text(b.id) }))
		.sort((a, b) => a.name.localeCompare(b.name));
}

/** The account's Skool groups. */
export async function getSkoolGroups(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const options = await networkOptions.call(this, 'skool');
	const groups = Array.isArray(options.groups) ? (options.groups as IDataObject[]) : [];
	return groups
		.filter((g) => text(g.id) !== '')
		.map((g) => ({ name: text(g.name) || text(g.slug) || text(g.id), value: text(g.id) }))
		.sort((a, b) => a.name.localeCompare(b.name));
}
