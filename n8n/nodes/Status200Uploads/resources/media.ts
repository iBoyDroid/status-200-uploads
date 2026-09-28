import type { INodeProperties } from 'n8n-workflow';
import { IDEMPOTENCY_OPTIONS, WAIT_OPTIONS } from './common';
import { routingFor } from './routing';

const forMedia = { resource: ['media'] };
const forImport = { resource: ['media'], operation: ['importFromUrl'] };
const forGet = { resource: ['media'], operation: ['get'] };

export const mediaOperation: INodeProperties = {
	displayName: 'Operation',
	name: 'operation',
	type: 'options',
	noDataExpression: true,
	displayOptions: { show: forMedia },
	options: [
		{
			name: 'Get',
			value: 'get',
			action: 'Get the status of an import',
			description: 'Read how an import is going',
			routing: routingFor('media.get'),
		},
		{
			name: 'Import From URL',
			value: 'importFromUrl',
			action: 'Import media from a URL',
			description: 'Import an image or a video from a public URL, for Post: Create',
			routing: routingFor('media.importFromUrl'),
		},
	],
	default: 'importFromUrl',
};

export const mediaFields: INodeProperties[] = [
	{
		displayName: 'URL',
		name: 'url',
		type: 'string',
		required: true,
		default: '',
		placeholder: 'e.g. https://example.com/video.mp4',
		displayOptions: { show: forImport },
		description:
			'The public http or https URL of the image or video file itself (JPG, PNG, WebP, MP4, MOV, WebM), not a web page that shows it. Images up to 20 MB, videos up to 5 GB.',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions: { show: forImport },
		options: [
			...IDEMPOTENCY_OPTIONS,
			...WAIT_OPTIONS.filter((o) => o.name === 'maxWait'),
			{
				displayName: 'Wait Until Ready',
				name: 'waitUntilReady',
				type: 'boolean',
				default: true,
				description:
					'Whether to wait, within Max Wait, until the file is ready to post. Off: output the import as it is (processing or ready).',
			},
			...WAIT_OPTIONS.filter((o) => o.name === 'waitWhenAsked'),
		],
	},
	{
		displayName: 'File ID',
		name: 'fileId',
		type: 'string',
		required: true,
		default: '',
		placeholder: 'e.g. a1b2c3d4-e5f6-7890-abcd-ef1234567890',
		displayOptions: { show: forGet },
		description: 'The file_id of Media: Import From URL',
	},
];
