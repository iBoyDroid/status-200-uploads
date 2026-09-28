#!/usr/bin/env node
// Checks what `npm pack` puts in the n8n package: only the built code (dist/), package.json, README.md
// and LICENSE.md, including every node and credential that package.json's "n8n" section names and the
// icons. Sources, tests and templates never ship. CI and the release (.github/workflows/ci.yml,
// publish-n8n.yml) both run it.
//
//   cd n8n && npm pack --dry-run --json > ../pack.json && node ../scripts/check-n8n-pack.mjs ../pack.json

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const packJsonPath = process.argv[2];
if (!packJsonPath) {
	console.error('Usage: node scripts/check-n8n-pack.mjs <file with the output of npm pack --json>');
	process.exit(2);
}

const [pack] = JSON.parse(readFileSync(packJsonPath, 'utf8'));
const pkg = JSON.parse(
	readFileSync(fileURLToPath(new URL('../n8n/package.json', import.meta.url)), 'utf8'),
);
const files = pack.files.map((f) => f.path).sort();
const TOP_LEVEL = ['package.json', 'README.md', 'LICENSE.md'];

const problems = [];
if (pack.name !== pkg.name || pack.version !== pkg.version) {
	problems.push(`packed ${pack.name}@${pack.version}, but n8n/package.json is ${pkg.name}@${pkg.version}`);
}
for (const file of files) {
	if (!file.startsWith('dist/') && !TOP_LEVEL.includes(file)) problems.push(`does not belong in the package: ${file}`);
	if (/(^|\/)(test|templates)\/|\.test\.|\.tsbuildinfo$|(^|\/)\.env/.test(file)) problems.push(`must not ship: ${file}`);
}
for (const file of [...TOP_LEVEL, ...pkg.n8n.nodes, ...pkg.n8n.credentials]) {
	if (!files.includes(file)) problems.push(`missing: ${file}`);
}
if (!files.some((file) => /^dist\/icons\/[^/]+\.svg$/.test(file))) problems.push('missing: the icons (dist/icons/*.svg)');

console.log(`${pack.filename}: ${files.length} files`);
for (const file of files) console.log(`  ${file}`);
if (problems.length > 0) {
	for (const problem of problems) console.error(`::error::${problem}`);
	process.exit(1);
}
console.log('The package holds exactly what it should.');
