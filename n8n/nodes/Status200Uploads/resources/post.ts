import type { INodeProperties } from 'n8n-workflow';
import { IDEMPOTENCY_OPTIONS, PLATFORM_OPTIONS, WAIT_OPTIONS } from './common';
import { accountLocator, postLocator } from './locators';
import { routingFor } from './routing';

const forPost = { resource: ['post'] };
const forCreate = { resource: ['post'], operation: ['create'] };
const forGet = { resource: ['post'], operation: ['get'] };
const forGetAll = { resource: ['post'], operation: ['getAll'] };
const forCancel = { resource: ['post'], operation: ['cancel'] };
const onPlatform = (platform: string) => ({ show: { ...forCreate, platform: [platform] } });

export const postOperation: INodeProperties = {
	displayName: 'Operation',
	name: 'operation',
	type: 'options',
	noDataExpression: true,
	displayOptions: { show: forPost },
	options: [
		{
			name: 'Cancel',
			value: 'cancel',
			action: 'Cancel a scheduled post',
			description: 'Stop a post that has not gone out yet (scheduled or queued)',
			routing: routingFor('post.cancel'),
		},
		{
			name: 'Create',
			value: 'create',
			action: 'Create a post',
			description: 'Publish a post now, schedule it, or only check it',
			routing: routingFor('post.create'),
		},
		{
			name: 'Get',
			value: 'get',
			action: 'Get a post',
			description: 'Read a post or a scheduled post and how it went',
			routing: routingFor('post.get'),
		},
		{
			name: 'Get Many',
			value: 'getAll',
			action: 'Get many posts',
			description: 'List your posts and scheduled posts, newest first',
			routing: routingFor('post.getAll'),
		},
	],
	default: 'create',
};

const createFields: INodeProperties[] = [
	{ ...accountLocator(true), displayOptions: { show: forCreate } },
	{
		displayName: 'Platform',
		name: 'platform',
		type: 'options',
		required: true,
		default: 'facebook',
		displayOptions: { show: forCreate },
		options: PLATFORM_OPTIONS,
		description:
			'The network to post to. One network per item: use one node per network to cross-post.',
	},
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		default: '',
		typeOptions: { rows: 4 },
		displayOptions: { show: forCreate },
		description: 'The caption, post text or title. Needed when the post has no media.',
	},
	{
		displayName: 'Media',
		name: 'media',
		type: 'options',
		default: 'none',
		displayOptions: { show: forCreate },
		options: [
			{
				name: 'File IDs',
				value: 'fileIds',
				description: 'Files imported with Media: Import From URL',
			},
			{ name: 'Media URLs', value: 'urls', description: 'Public URLs of the files' },
			{
				name: 'None',
				value: 'none',
				description: 'A text post (X, LinkedIn, Threads, Skool and Facebook)',
			},
		],
	},
	{
		displayName:
			'Media is sent by URL. To post a file from an earlier node (binary data), first store it at a public URL (for example S3, a Google Drive or Dropbox share, or Cloudinary).',
		name: 'mediaNotice',
		type: 'notice',
		default: '',
		displayOptions: { show: { ...forCreate, media: ['urls'] } },
	},
	{
		displayName: 'Media URLs',
		name: 'mediaUrls',
		type: 'string',
		default: '',
		required: true,
		typeOptions: { rows: 3 },
		placeholder: 'e.g. https://example.com/photo.jpg',
		displayOptions: { show: { ...forCreate, media: ['urls'] } },
		description:
			'Public URLs of the image or video files, one per line. Whether each is an image or a video is read from the end of its URL (.jpg, .png, .mp4 ...).',
	},
	{
		displayName: 'File IDs',
		name: 'fileIds',
		type: 'string',
		default: '',
		required: true,
		placeholder: 'e.g. a1b2c3d4-e5f6-7890-abcd-ef1234567890',
		displayOptions: { show: { ...forCreate, media: ['fileIds'] } },
		description: 'The file_id of each imported file, one per line or separated by commas',
	},
	{
		displayName: 'When',
		name: 'when',
		type: 'options',
		default: 'now',
		displayOptions: { show: forCreate },
		options: [
			{ name: 'At a Set Time', value: 'later', description: 'Schedule it (up to 365 days ahead)' },
			{ name: 'Now', value: 'now', description: 'Publish it now' },
		],
	},
	{
		displayName: 'Scheduled For',
		name: 'scheduledFor',
		type: 'dateTime',
		default: '',
		required: true,
		displayOptions: { show: { ...forCreate, when: ['later'] } },
		description:
			'When to publish. A date and time without a time zone is read in the time zone of this workflow (its settings).',
	},
	{
		displayName: 'TikTok Privacy Level Name or ID',
		name: 'tiktokPrivacyLevel',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getTikTokPrivacyLevels',
			loadOptionsDependsOn: ['account.value'],
		},
		displayOptions: onPlatform('tiktok'),
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		hint: 'Who can see the video. Only the levels this TikTok account allows are listed.',
	},
	{
		displayName: 'YouTube Privacy Status',
		name: 'youtubePrivacyStatus',
		type: 'options',
		required: true,
		default: 'private',
		displayOptions: onPlatform('youtube'),
		options: [
			{ name: 'Private', value: 'private' },
			{ name: 'Public', value: 'public' },
			{ name: 'Unlisted', value: 'unlisted' },
		],
		description: 'Who can see the video on YouTube',
	},
	{
		displayName: 'Pinterest Board Name or ID',
		name: 'pinterestBoardId',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getPinterestBoards',
			loadOptionsDependsOn: ['account.value'],
		},
		displayOptions: onPlatform('pinterest'),
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		hint: 'The board to pin to',
	},
	{
		displayName: 'Skool Group Name or ID',
		name: 'skoolGroup',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getSkoolGroups',
			loadOptionsDependsOn: ['account.value'],
		},
		displayOptions: onPlatform('skool'),
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		hint: 'The group to post in',
	},
	{
		displayName: 'Skool Title',
		name: 'skoolTitle',
		type: 'string',
		required: true,
		default: '',
		displayOptions: onPlatform('skool'),
		description: 'The title of the Skool post',
	},
	{
		displayName: 'TikTok Options',
		name: 'tiktokOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('tiktok'),
		options: [
			{
				displayName: 'AI-Generated Content',
				name: 'isAiGenerated',
				type: 'boolean',
				default: false,
				description: 'Whether to label the video as made with AI (videos only)',
			},
			{
				displayName: 'Auto Add Music',
				name: 'autoAddMusic',
				type: 'boolean',
				default: false,
				description: 'Whether TikTok adds recommended music (photo posts only)',
			},
			{
				displayName: 'Branded Content',
				name: 'isBrandedContent',
				type: 'boolean',
				default: false,
				description: 'Whether the post promotes a third party (a paid partnership)',
			},
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description:
					'The description of a photo post, up to 4,000 characters. Not used on a video.',
			},
			{
				displayName: 'Disable Comments',
				name: 'disabledComments',
				type: 'boolean',
				default: false,
				description: 'Whether to turn comments off',
			},
			{
				displayName: 'Disable Duet',
				name: 'disabledDuet',
				type: 'boolean',
				default: false,
				description: 'Whether to turn Duet off (videos only)',
			},
			{
				displayName: 'Disable Stitch',
				name: 'disabledStitch',
				type: 'boolean',
				default: false,
				description: 'Whether to turn Stitch off (videos only)',
			},
			{
				displayName: 'Promotes Your Own Brand',
				name: 'isYourBrand',
				type: 'boolean',
				default: false,
				description: 'Whether the post promotes your own business',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description:
					'The title of a photo post, up to 90 characters. On a video it is the caption, instead of Text.',
			},
		],
	},
	{
		displayName: 'Instagram Options',
		name: 'instagramOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('instagram'),
		options: [
			{
				displayName: 'Collaborators',
				name: 'collaborators',
				type: 'string',
				default: '',
				description: 'Usernames to invite as collaborators, separated by commas',
			},
			{
				displayName: 'Cover URL',
				name: 'coverUrl',
				type: 'string',
				default: '',
				description: 'The URL of a cover image for a Reel',
			},
			{
				displayName: 'Location ID',
				name: 'locationId',
				type: 'string',
				default: '',
				description: 'A Facebook location ID (feed images)',
			},
			{
				displayName: 'Post Type',
				name: 'postType',
				type: 'options',
				default: 'feed_image',
				options: [
					{ name: 'Carousel', value: 'carousel' },
					{ name: 'Feed Image', value: 'feed_image' },
					{ name: 'Reel', value: 'reel' },
					{ name: 'Story', value: 'story' },
				],
				description:
					'Left out: carousel for two or more files, reel for a single video, otherwise feed image',
			},
			{
				displayName: 'Share Reel to Feed',
				name: 'shareToFeed',
				type: 'boolean',
				default: true,
				description: 'Whether a Reel also shows in the feed',
			},
			{
				displayName: 'Thumbnail Offset (Ms)',
				name: 'thumbOffset',
				type: 'number',
				default: 0,
				typeOptions: { minValue: 0 },
				description: 'Where in a Reel its thumbnail is taken from, in milliseconds',
			},
		],
	},
	{
		displayName: 'Facebook Options',
		name: 'facebookOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('facebook'),
		options: [
			{
				displayName: 'Link',
				name: 'url',
				type: 'string',
				default: '',
				description: 'A link for a text post (Facebook shows a preview of it)',
			},
			{
				displayName: 'Post Type',
				name: 'postType',
				type: 'options',
				default: 'photo',
				options: [
					{ name: 'Photo', value: 'photo' },
					{ name: 'Reel', value: 'reel' },
					{ name: 'Text', value: 'text' },
					{ name: 'Video', value: 'video' },
				],
				description:
					'Left out: text when there is no media, video for one video file, otherwise photo',
			},
			{
				displayName: 'Video Title',
				name: 'videoTitle',
				type: 'string',
				default: '',
				description: 'The title of a video post (the text when left out)',
			},
		],
	},
	{
		displayName: 'YouTube Options',
		name: 'youtubeOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('youtube'),
		options: [
			{
				displayName: 'Category ID',
				name: 'categoryId',
				type: 'string',
				default: '22',
				description: 'The YouTube category (22 is People & Blogs)',
			},
			{
				displayName: 'Default Language',
				name: 'defaultLanguage',
				type: 'string',
				default: '',
				placeholder: 'e.g. en',
				description: 'The language of the title and description',
			},
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				typeOptions: { rows: 3 },
				description:
					'The description, up to 5,000 bytes. Left out, Text is used when a title is set.',
			},
			{
				displayName: 'Embeddable',
				name: 'embeddable',
				type: 'boolean',
				default: true,
				description: 'Whether the video can be embedded on other sites',
			},
			{
				displayName: 'License',
				name: 'license',
				type: 'options',
				default: 'youtube',
				options: [
					{ name: 'Creative Commons', value: 'creativeCommon' },
					{ name: 'Standard YouTube License', value: 'youtube' },
				],
			},
			{
				displayName: 'Made for Kids',
				name: 'madeForKids',
				type: 'boolean',
				default: false,
				description: 'Whether the video is made for children',
			},
			{
				displayName: 'Notify Subscribers',
				name: 'notifySubscribers',
				type: 'boolean',
				default: true,
				description: 'Whether subscribers are told about the video',
			},
			{
				displayName: 'Public Stats Viewable',
				name: 'publicStatsViewable',
				type: 'boolean',
				default: true,
				description: 'Whether the view count and the other figures are public',
			},
			{
				displayName: 'Tags',
				name: 'tags',
				type: 'string',
				default: '',
				description: 'Tags separated by commas (500 characters in all)',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'The title, up to 100 characters. Left out, it comes from Text.',
			},
		],
	},
	{
		displayName: 'X Options',
		name: 'xOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('x'),
		options: [
			{
				displayName: 'Community URL',
				name: 'community',
				type: 'string',
				default: '',
				placeholder: 'e.g. https://x.com/i/communities/1234567890',
				description: 'Post into this X community',
			},
			{
				displayName: 'Text for X',
				name: 'text',
				type: 'string',
				default: '',
				description: 'Used on X instead of Text',
			},
			{
				displayName: 'Who Can Reply',
				name: 'whoCanReply',
				type: 'options',
				default: 'everyone',
				options: [
					{ name: 'Everyone', value: 'everyone' },
					{ name: 'Mentioned Users', value: 'mentionedUsers' },
					{ name: 'People You Follow', value: 'following' },
					{ name: 'Subscribers', value: 'subscribers' },
					{ name: 'Verified Accounts', value: 'verified' },
				],
			},
		],
	},
	{
		displayName: 'LinkedIn Options',
		name: 'linkedinOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('linkedin'),
		options: [
			{
				displayName: 'Text for LinkedIn',
				name: 'text',
				type: 'string',
				default: '',
				description: 'Used on LinkedIn instead of Text',
			},
		],
	},
	{
		displayName: 'Pinterest Options',
		name: 'pinterestOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('pinterest'),
		options: [
			{
				displayName: 'Alt Text',
				name: 'altText',
				type: 'string',
				default: '',
				description: 'A description of the image for people who cannot see it',
			},
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description: 'Up to 800 characters',
			},
			{
				displayName: 'Dominant Color',
				name: 'dominantColor',
				type: 'color',
				default: '',
				description: 'A hex color shown while the pin loads',
			},
			{
				displayName: 'Link',
				name: 'link',
				type: 'string',
				default: '',
				description: 'Where the pin leads',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'Up to 100 characters. Left out, it comes from Text.',
			},
		],
	},
	{
		displayName: 'Threads Options',
		name: 'threadsOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('threads'),
		options: [
			{
				displayName: 'Text for Threads',
				name: 'text',
				type: 'string',
				default: '',
				description: 'Used on Threads instead of Text (up to 500 characters)',
			},
		],
	},
	{
		displayName: 'Skool Options',
		name: 'skoolOptions',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: onPlatform('skool'),
		options: [
			{
				displayName: 'Group Slug',
				name: 'groupSlug',
				type: 'string',
				default: '',
				description: 'The group in its web address, e.g. my-group',
			},
			{
				displayName: 'Label ID',
				name: 'label',
				type: 'string',
				default: '',
				description: 'A category label (some groups need one)',
			},
		],
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: { show: forCreate },
		options: [
			{
				displayName: 'Additional Post Fields',
				name: 'additionalPostFields',
				type: 'json',
				default: '{}',
				description:
					'More fields for the post, merged in last, for choices this node does not show yet. For example {"tiktok": {"isAiGenerated": true}}.',
			},
			{
				displayName: 'Check Only (Dry Run)',
				name: 'dryRun',
				type: 'boolean',
				default: false,
				description:
					'Whether to run every check a publish makes and send nothing. The answer is a report with dry_run true.',
			},
			...IDEMPOTENCY_OPTIONS,
			...WAIT_OPTIONS,
		],
	},
];

const getFields: INodeProperties[] = [
	{ ...postLocator('post', 'Post', 'searchPosts'), displayOptions: { show: forGet } },
];

const cancelFields: INodeProperties[] = [
	{
		...postLocator('scheduledPost', 'Scheduled Post', 'searchScheduledPosts'),
		displayOptions: { show: forCancel },
	},
];

const getAllFields: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		displayOptions: { show: forGetAll },
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		typeOptions: { minValue: 1, maxValue: 100 },
		displayOptions: { show: { ...forGetAll, returnAll: [false] } },
		description: 'Max number of results to return',
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: { show: forGetAll },
		options: [
			{
				displayName: 'Kind',
				name: 'kind',
				type: 'options',
				default: 'post',
				options: [
					{ name: 'Post', value: 'post', description: 'Posts sent to a network' },
					{
						name: 'Scheduled Post',
						value: 'scheduled_post',
						description: 'Posts waiting to go out',
					},
				],
			},
			{
				displayName: 'Platform',
				name: 'platform',
				type: 'options',
				default: 'facebook',
				options: PLATFORM_OPTIONS,
			},
			{
				displayName: 'Profile ID',
				name: 'profileId',
				type: 'string',
				default: '',
				placeholder: 'e.g. d4e5f6a7-b8c9-0123-def0-234567890123',
				description: 'Only this profile (profile_id of Account: Get Many)',
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'multiOptions',
				default: [],
				options: [
					{ name: 'Cancelled', value: 'cancelled' },
					{ name: 'Failed', value: 'failed' },
					{ name: 'Processing', value: 'processing' },
					{ name: 'Scheduled', value: 'scheduled' },
					{ name: 'Success', value: 'success' },
					{ name: 'Timeout', value: 'timeout' },
				],
				description:
					'Success, processing and timeout are posts; scheduled and cancelled are scheduled posts; failed is both',
			},
		],
	},
];

const simplifyField: INodeProperties = {
	displayName: 'Simplify',
	name: 'simplify',
	type: 'boolean',
	default: true,
	displayOptions: { show: { resource: ['post'], operation: ['get', 'getAll'] } },
	description: 'Whether to return a simplified version of the response instead of the raw data',
};

export const postFields: INodeProperties[] = [
	...createFields,
	...getFields,
	...cancelFields,
	...getAllFields,
	simplifyField,
];
