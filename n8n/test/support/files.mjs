// File access for the tests. It is plain JavaScript on purpose: n8n's lint rules for community nodes
// (no node:fs, no process) are written for the code that runs inside n8n, and these tests never ship
// (package.json "files" is dist only; n8n's scanner lints only nodes/, credentials/ and package.json).

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

/** The n8n package folder. */
export const PACKAGE_ROOT = fileURLToPath(new URL('../..', import.meta.url));

/** The copy of the API description at the root of the repository. */
export const SPEC_PATH = fileURLToPath(new URL('../../../openapi/openapi.yaml', import.meta.url));

/** A file of the package, as text. */
export function readPackageFile(path) {
	return readFileSync(join(PACKAGE_ROOT, path), 'utf8');
}

/** The OpenAPI file, as text. */
export function readSpecText() {
	return readFileSync(SPEC_PATH, 'utf8');
}

/** Whether a file of the package exists. */
export function packageFileExists(path) {
	return existsSync(join(PACKAGE_ROOT, path));
}

/** Every file under a folder of the package, as paths relative to the package with forward slashes. */
export function listPackageFiles(folder) {
	const out = [];
	const walk = (dir) => {
		for (const name of readdirSync(dir)) {
			const full = join(dir, name);
			if (statSync(full).isDirectory()) walk(full);
			else out.push(relative(PACKAGE_ROOT, full).split(sep).join('/'));
		}
	};
	walk(join(PACKAGE_ROOT, folder));
	return out.sort();
}
