import type { INodeProperties } from 'n8n-workflow';
import {
	DEFAULT_MAX_WAIT_SECONDS,
	MAX_WAIT_LIMIT_SECONDS,
	PLATFORM_NAMES,
	PLATFORMS,
} from '../shared/constants';

/** The networks as options, sorted by name. */
export const PLATFORM_OPTIONS = PLATFORMS.map((value) => ({
	name: PLATFORM_NAMES[value],
	value,
})).sort((a, b) => a.name.localeCompare(b.name));

/** The Idempotency Key choices of a POST (inside an Options collection). */
export const IDEMPOTENCY_OPTIONS: INodeProperties[] = [
	{
		displayName: 'Custom Idempotency Key',
		name: 'customIdempotencyKey',
		type: 'string',
		default: '',
		placeholder: 'e.g. {{ $json.guid }}-tiktok',
		displayOptions: { show: { idempotencyKeyMode: ['custom'] } },
		description:
			'1 to 255 printable characters that name this request across runs. The same key with the same request within 24 hours gets the first answer back. Never build it from $now or a random value.',
	},
	{
		displayName: 'Idempotency Key',
		name: 'idempotencyKeyMode',
		type: 'options',
		default: 'auto',
		description: 'The key that makes sending this request again safe',
		options: [
			{
				name: 'Automatic',
				value: 'auto',
				description:
					'Made from the workflow, the execution, the node, the item and the request. Resends by the node always reuse it; Retry On Fail does too, as long as no field uses $now or a random value.',
			},
			{
				name: 'Custom',
				value: 'custom',
				description: 'Your own key, for example from the ID of the row or file being posted',
			},
			{
				name: 'Off',
				value: 'off',
				description: 'No key: a request sent twice is done twice',
			},
		],
	},
];

/** Max Wait and Wait When Asked (inside an Options collection). */
export const WAIT_OPTIONS: INodeProperties[] = [
	{
		displayName: 'Max Wait (Seconds)',
		name: 'maxWait',
		type: 'number',
		default: DEFAULT_MAX_WAIT_SECONDS,
		typeOptions: { minValue: 0, maxValue: MAX_WAIT_LIMIT_SECONDS },
		description:
			'The most this item waits in all when the API asks it to wait (a file still importing, a rate limit), up to 600',
	},
	{
		displayName: 'Wait When Asked',
		name: 'waitWhenAsked',
		type: 'boolean',
		default: true,
		description:
			'Whether to wait and send the same request again when the API asks for it (Retry-After), within Max Wait. Off: stop with the answer instead.',
	},
];
