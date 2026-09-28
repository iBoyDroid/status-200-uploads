import { NodeConnectionTypes, type INodeType, type INodeTypeDescription } from 'n8n-workflow';
import { accountFields, accountOperation } from './resources/account';
import { mediaFields, mediaOperation } from './resources/media';
import { postFields, postOperation } from './resources/post';
import { API_BASE_URL, CREDENTIAL_TYPE } from './shared/constants';
import {
	getPinterestBoards,
	getSkoolGroups,
	getTikTokPrivacyLevels,
	searchAccounts,
	searchPosts,
	searchScheduledPosts,
} from './shared/methods';
import { DEFAULT_HEADERS } from './shared/transport';

export class Status200Uploads implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Status 200 Uploads',
		name: 'status200Uploads',
		icon: {
			light: 'file:../../icons/status200uploads.svg',
			dark: 'file:../../icons/status200uploads.dark.svg',
		},
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description:
			'Publish and schedule posts to TikTok, Instagram, Facebook, YouTube, X, LinkedIn, Pinterest, Threads and Skool',
		defaults: {
			name: 'Status 200 Uploads',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: CREDENTIAL_TYPE,
				required: true,
			},
		],
		requestDefaults: {
			baseURL: API_BASE_URL,
			headers: { ...DEFAULT_HEADERS },
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Account',
						value: 'account',
					},
					{
						name: 'Media',
						value: 'media',
					},
					{
						name: 'Post',
						value: 'post',
					},
				],
				default: 'post',
			},
			postOperation,
			accountOperation,
			mediaOperation,
			...postFields,
			...accountFields,
			...mediaFields,
		],
	};

	methods = {
		listSearch: {
			searchAccounts,
			searchPosts,
			searchScheduledPosts,
		},
		loadOptions: {
			getPinterestBoards,
			getSkoolGroups,
			getTikTokPrivacyLevels,
		},
	};
}
