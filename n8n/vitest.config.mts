import { defineConfig } from 'vitest/config';

// Tests live in test/, never under nodes/ or credentials/ (those folders are what n8n loads and what
// n8n's scanner lints). They read ../openapi/openapi.yaml, the copy of the API description.
export default defineConfig({
	test: {
		include: ['test/**/*.test.ts'],
		environment: 'node',
	},
});
