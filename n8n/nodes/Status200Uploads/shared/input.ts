/**
 * A parameter of the node cannot be sent as it is. The n8n layer turns it into a NodeOperationError
 * (message: what is wrong with it; description: how to change it), so the pure request code stays
 * free of n8n and testable on its own.
 */
export class InvalidInput extends Error {
	readonly description: string;

	constructor(message: string, description: string) {
		super(message);
		this.name = 'InvalidInput';
		this.description = description;
	}
}
