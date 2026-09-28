import type { INodeProperties } from 'n8n-workflow';
import { UUID_PATTERN } from '../shared/constants';

const UUID_ONLY = `^${UUID_PATTERN}$`;
const POST_URL = `https:\\/\\/status200uploads\\.com\\/api\\/v2\\/posts\\/(${UUID_PATTERN})`;

/** A profile: from the list (GET /accounts), by ID, or (where the API takes one) by @handle. */
export function accountLocator(withHandle: boolean): Omit<INodeProperties, 'displayOptions'> {
	return {
		displayName: 'Account',
		name: withHandle ? 'account' : 'profile',
		type: 'resourceLocator',
		default: { mode: 'list', value: '' },
		required: true,
		description: 'The profile, as on the Connections page of your dashboard',
		modes: [
			{
				displayName: 'From List',
				name: 'list',
				type: 'list',
				placeholder: 'Select an account...',
				typeOptions: {
					searchListMethod: 'searchAccounts',
					searchable: true,
				},
			},
			{
				displayName: 'By ID',
				name: 'id',
				type: 'string',
				placeholder: 'e.g. d4e5f6a7-b8c9-0123-def0-234567890123',
				validation: [
					{
						type: 'regex',
						properties: {
							regex: UUID_ONLY,
							errorMessage: 'Not a profile ID (profile_id of Account: Get Many)',
						},
					},
				],
			},
			...(withHandle
				? [
						{
							displayName: 'By Handle',
							name: 'handle',
							type: 'string' as const,
							placeholder: 'e.g. @myprofile',
							validation: [
								{
									type: 'regex' as const,
									properties: {
										regex: '^@?\\S.*$',
										errorMessage: 'Not a profile handle',
									},
								},
							],
						},
					]
				: []),
		],
	};
}

/** A post or scheduled post: from the list, by ID, or by its status_url. */
export function postLocator(
	name: string,
	displayName: string,
	searchListMethod: string,
): Omit<INodeProperties, 'displayOptions'> {
	return {
		displayName,
		name,
		type: 'resourceLocator',
		default: { mode: 'list', value: '' },
		required: true,
		modes: [
			{
				displayName: 'From List',
				name: 'list',
				type: 'list',
				placeholder: 'Select a post...',
				typeOptions: {
					searchListMethod,
					searchable: true,
				},
			},
			{
				displayName: 'By ID',
				name: 'id',
				type: 'string',
				placeholder: 'e.g. c3d4e5f6-a7b8-9012-cdef-123456789012',
				validation: [
					{
						type: 'regex',
						properties: {
							regex: UUID_ONLY,
							errorMessage: 'Not an ID of Status 200 Uploads',
						},
					},
				],
			},
			{
				displayName: 'By URL',
				name: 'url',
				type: 'string',
				placeholder:
					'e.g. https://status200uploads.com/api/v2/posts/c3d4e5f6-a7b8-9012-cdef-123456789012',
				extractValue: {
					type: 'regex',
					regex: POST_URL,
				},
				validation: [
					{
						type: 'regex',
						properties: {
							regex: `${POST_URL}.*`,
							errorMessage: 'Not a status_url of Status 200 Uploads',
						},
					},
				],
			},
		],
	};
}
