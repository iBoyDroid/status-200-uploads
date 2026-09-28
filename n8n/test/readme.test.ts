// The README's example workflow must import: valid JSON, this package's node type, parameters that
// n8n resolves, and nothing missing but the account the reader chooses.

import { NodeHelpers, type INodeProperties } from 'n8n-workflow';
import { describe, expect, it } from 'vitest';
import { description, makeNode, resolveParameters } from './support/fake';
import { readPackageFile } from './support/files.mjs';

interface WorkflowNode {
	name: string;
	type: string;
	typeVersion: number;
	parameters: Record<string, unknown>;
}

const readme = readPackageFile('README.md');
const blocks = [...readme.matchAll(/```json\n([\s\S]*?)```/g)].map((m) => m[1]);

describe('README', () => {
	it('has one example workflow, and it is valid JSON', () => {
		expect(blocks).toHaveLength(1);
		expect(() => JSON.parse(blocks[0]) as unknown).not.toThrow();
	});

	it('its Status 200 Uploads nodes resolve, missing only the account to choose', () => {
		const workflow = JSON.parse(blocks[0]) as {
			nodes: WorkflowNode[];
			connections: Record<string, unknown>;
		};
		const ours = workflow.nodes.filter(
			(n) => n.type === '@status200uploads/n8n-nodes-status200uploads.status200Uploads',
		);
		expect(ours.length).toBeGreaterThan(0);
		for (const node of ours) {
			expect(node.typeVersion).toBe(1);
			const parameters = resolveParameters(node.parameters);
			expect(parameters).toMatchObject({ resource: 'post', operation: 'create' });
			const issues = NodeHelpers.getNodeParametersIssues(
				description.properties as INodeProperties[],
				makeNode(parameters),
				description,
			);
			expect(Object.keys(issues?.parameters ?? {}), node.name).toEqual(['account']);
			expect(workflow.connections).toHaveProperty(['When clicking Execute workflow']);
		}
	});

	it('names the package as npm and n8n know it', () => {
		expect(readme).toContain('@status200uploads/n8n-nodes-status200uploads');
		expect(readme).not.toMatch(/rl_[0-9a-f]{8,}/);
	});
});
