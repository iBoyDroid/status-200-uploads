import type { INodePropertyRouting } from 'n8n-workflow';
import { handleAnswer, prepareRequest } from '../shared/hooks';
import { ENDPOINTS, type Operation } from '../shared/request';

/**
 * The routing of every operation: its method and path (ENDPOINTS), then one preSend that builds the
 * whole request and one postReceive that reads the answer. HTTP statuses never throw: handleAnswer
 * decides what each answer means.
 */
export function routingFor(operation: Operation): INodePropertyRouting {
	const { method, path } = ENDPOINTS[operation];
	return {
		request: {
			method,
			url: path,
			ignoreHttpStatusErrors: true,
			returnFullResponse: true,
		},
		send: {
			preSend: [prepareRequest],
		},
		output: {
			postReceive: [handleAnswer],
		},
	};
}
