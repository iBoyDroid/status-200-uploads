import type { INodeProperties } from 'n8n-workflow';
import { PLATFORM_OPTIONS } from './common';
import { accountLocator } from './locators';
import { routingFor } from './routing';

const forAccount = { resource: ['account'] };
const forGetAll = { resource: ['account'], operation: ['getAll'] };
const forOptions = { resource: ['account'], operation: ['getPostingOptions'] };

export const accountOperation: INodeProperties = {
	displayName: 'Operation',
	name: 'operation',
	type: 'options',
	noDataExpression: true,
	displayOptions: { show: forAccount },
	options: [
		{
			name: 'Get Many',
			value: 'getAll',
			action: 'Get many accounts',
			description: 'List your profiles and their connected networks',
			routing: routingFor('account.getAll'),
		},
		{
			name: 'Get Posting Options',
			value: 'getPostingOptions',
			action: 'Get the posting options of an account',
			description:
				'What a profile may do on each network: TikTok privacy levels, Pinterest boards, Skool groups and more',
			routing: routingFor('account.getPostingOptions'),
		},
	],
	default: 'getAll',
};

export const accountFields: INodeProperties[] = [
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
	{ ...accountLocator(false), displayOptions: { show: forOptions } },
	{
		displayName: 'Platforms',
		name: 'platforms',
		type: 'multiOptions',
		default: [],
		displayOptions: { show: forOptions },
		options: PLATFORM_OPTIONS,
		description: 'Only these networks. None chosen: every connected network.',
	},
	{
		displayName: 'Skool Group Slug',
		name: 'skoolGroupSlug',
		type: 'string',
		default: '',
		placeholder: 'e.g. my-group',
		displayOptions: { show: forOptions },
		description: 'Which Skool group to read the labels of (with one group, its labels come anyway)',
	},
];
