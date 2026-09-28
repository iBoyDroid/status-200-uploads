import type {
	IAuthenticateGeneric,
	Icon,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';
import { API_BASE_URL, USER_AGENT } from '../nodes/Status200Uploads/shared/constants';

export class Status200UploadsApi implements ICredentialType {
	name = 'status200UploadsApi';

	displayName = 'Status 200 Uploads API';

	icon: Icon = {
		light: 'file:../icons/status200uploads.svg',
		dark: 'file:../icons/status200uploads.dark.svg',
	};

	documentationUrl = 'https://status200uploads.com/docs/api#authentication';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
			description:
				'An API key from your Status 200 Uploads dashboard, API page. It starts with rl_. Anyone with it can post as you: keep it in this credential only.',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiKey}}',
			},
		},
	};

	/** GET /api/v2/accounts: 200 with a good key, 401 unauthorized otherwise. */
	test: ICredentialTestRequest = {
		request: {
			baseURL: API_BASE_URL,
			url: '/accounts',
			method: 'GET',
			headers: {
				Accept: 'application/json',
				'User-Agent': USER_AGENT,
			},
		},
	};
}
