// What n8n's verification and npm's provenance check look at, and what the scanner cannot be told
// to skip.

import { describe, expect, it } from 'vitest';
import { PACKAGE_VERSION, USER_AGENT } from '../nodes/Status200Uploads/shared/constants';
import { listPackageFiles, packageFileExists, readPackageFile } from './support/files.mjs';

const pkg = JSON.parse(readPackageFile('package.json')) as Record<string, unknown> & {
	n8n: { credentials: string[]; nodes: string[]; strict: boolean; n8nNodesApiVersion: number };
};

describe('package.json', () => {
	it('the User-Agent carries the package version', () => {
		expect(PACKAGE_VERSION).toBe(pkg.version);
		expect(USER_AGENT).toBe(`n8n-nodes-status200uploads/${String(pkg.version)}`);
	});

	it('names the package, the author and the repository exactly as npm and n8n check them', () => {
		expect(pkg.name).toBe('@status200uploads/n8n-nodes-status200uploads');
		expect(pkg.license).toBe('MIT');
		expect(pkg.author).toEqual({
			name: 'iBoyDroid',
			email: 'info@status200uploads.com',
			url: 'https://github.com/iBoyDroid',
		});
		expect(pkg.repository).toEqual({
			type: 'git',
			url: 'git+https://github.com/iBoyDroid/status-200-uploads.git',
			directory: 'n8n',
		});
		expect(pkg.keywords).toContain('n8n-community-node-package');
		expect(pkg.publishConfig).toEqual({ access: 'public', provenance: true });
		expect(pkg.files).toEqual(['dist', '!dist/tsconfig.tsbuildinfo']);
	});

	it('has no runtime dependencies, overrides or install scripts; n8n-workflow is a peer', () => {
		expect(pkg.dependencies).toBeUndefined();
		expect(pkg.overrides).toBeUndefined();
		expect(pkg.peerDependencies).toEqual({ 'n8n-workflow': '*' });
		const scripts = pkg.scripts as Record<string, string>;
		for (const hook of ['preinstall', 'install', 'postinstall', 'prepare'])
			expect(scripts[hook]).toBeUndefined();
		expect(scripts.prepublishOnly).toBe('n8n-node prerelease');
	});

	it('lists the node and the credential, whose sources exist', () => {
		expect(pkg.n8n).toMatchObject({ n8nNodesApiVersion: 1, strict: true });
		for (const built of [...pkg.n8n.nodes, ...pkg.n8n.credentials]) {
			expect(packageFileExists(built.replace(/^dist\//, '').replace(/\.js$/, '.ts')), built).toBe(
				true,
			);
		}
	});

	it('the codex file names this package', () => {
		const codex = JSON.parse(
			readPackageFile('nodes/Status200Uploads/Status200Uploads.node.json'),
		) as { node: string; categories: string[] };
		expect(codex.node).toBe(pkg.name);
		expect(codex.categories).toEqual(['Marketing & Content']);
	});

	it('eslint.config.mjs is n8n’s default (eligible for n8n Cloud)', () => {
		expect(readPackageFile('eslint.config.mjs').replace(/\s+/g, ' ').trim()).toBe(
			"import { config } from '@n8n/node-cli/eslint'; export default config;",
		);
	});
});

describe('the code n8n runs', () => {
	const sources = [...listPackageFiles('nodes'), ...listPackageFiles('credentials')].filter((f) =>
		f.endsWith('.ts'),
	);

	it('has no eslint-disable comments (n8n’s scanner ignores them, so every rule must really pass)', () => {
		for (const file of sources)
			expect(readPackageFile(file), file).not.toMatch(/eslint-disable|@ts-ignore|@ts-nocheck/);
	});

	it('reads no environment variable and no file, and calls only the API', () => {
		for (const file of sources) {
			const text = readPackageFile(file);
			expect(text, file).not.toMatch(/process\.env|from '(node:)?fs'|require\(/);
			for (const url of text.match(/https?:\/\/[^\s'"`)]+/g) ?? []) {
				expect(url, file).toMatch(
					/^https:\/\/(status200uploads\.com|docs\.n8n\.io|x\.com\/i\/communities|example\.com)/,
				);
			}
		}
	});

	it('keeps tests out of nodes/ and credentials/', () => {
		expect(sources.filter((f) => /\.test\.ts$|(^|\/)test\.ts$/.test(f))).toEqual([]);
	});
});
