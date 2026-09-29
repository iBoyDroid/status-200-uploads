/** The package version, sent in the User-Agent. test/package.test.ts holds it equal to package.json. */
export const PACKAGE_VERSION = '0.1.1';

/** Every request of this node says who sent it, so support can tell node traffic apart. */
export const USER_AGENT = `n8n-nodes-status200uploads/${PACKAGE_VERSION}`;

/** The only address this node calls (the OpenAPI file's top-level server). */
export const API_BASE_URL = 'https://status200uploads.com/api/v2';

/** The credential type every request is signed with. */
export const CREDENTIAL_TYPE = 'status200UploadsApi';

/** Where the node's documentation lives. */
export const DOCS_URL = 'https://status200uploads.com/docs/api#guide-n8n';

/** The networks, as components.schemas.Platform of the OpenAPI file lists them (sorted). */
export const PLATFORMS = [
	'facebook',
	'instagram',
	'linkedin',
	'pinterest',
	'skool',
	'threads',
	'tiktok',
	'x',
	'youtube',
] as const;

export type Platform = (typeof PLATFORMS)[number];

/** Display names of the networks. */
export const PLATFORM_NAMES: Record<Platform, string> = {
	facebook: 'Facebook',
	instagram: 'Instagram',
	linkedin: 'LinkedIn',
	pinterest: 'Pinterest',
	skool: 'Skool',
	threads: 'Threads',
	tiktok: 'TikTok',
	x: 'X',
	youtube: 'YouTube',
};

/**
 * The per-network fields the node shows on its own (not in the network's options collection), and where
 * each goes in the post: post.<platform>.<field>.
 */
export const REQUIRED_FIELDS: Record<string, { platform: Platform; field: string }> = {
	tiktokPrivacyLevel: { platform: 'tiktok', field: 'privacyLevel' },
	youtubePrivacyStatus: { platform: 'youtube', field: 'privacyStatus' },
	pinterestBoardId: { platform: 'pinterest', field: 'boardId' },
	skoolGroup: { platform: 'skool', field: 'group' },
	skoolTitle: { platform: 'skool', field: 'title' },
};

/** Option fields that the API takes as a list; the node takes them as comma-separated text. */
export const LIST_FIELDS: Record<string, string[]> = {
	instagram: ['collaborators'],
	youtube: ['tags'],
};

/** How long the node waits in all, by default, when the API asks it to wait (seconds). */
export const DEFAULT_MAX_WAIT_SECONDS = 120;

/** The most a node may wait in one item (seconds). */
export const MAX_WAIT_LIMIT_SECONDS = 600;

/** Reads and cancels wait at most this long (seconds): a read limit resets within a minute. */
export const READ_MAX_WAIT_SECONDS = 70;

/** Dropdowns in the editor wait at most this long (seconds). */
export const EDITOR_MAX_WAIT_SECONDS = 15;

/** How often an import is read while the node waits for it (seconds). */
export const MEDIA_POLL_SECONDS = 5;

/** A UUID, as the API's ids are. */
export const UUID_PATTERN =
	'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}';
