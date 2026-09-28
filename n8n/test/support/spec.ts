// The OpenAPI file (../openapi/openapi.yaml) as the tests read it: parsed, with an Ajv validator for
// any schema in it (JSON Schema 2020-12, OpenAPI 3.1's dialect), and its answers' examples.

import Ajv2020, { type ValidateFunction } from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import YAML from 'yaml';
import { readSpecText } from './files.mjs';

type Json = Record<string, unknown>;

export const spec = YAML.parse(readSpecText()) as Json & {
	servers: Array<{ url: string }>;
	paths: Record<string, Json>;
	components: Json & {
		schemas: Record<string, Json>;
		responses: Record<string, Json>;
		parameters: Record<string, Json>;
		'x-status200-retry': {
			version: number;
			rules: Record<string, string>;
			by_code: Record<string, string>;
			by_status: Record<string, string>;
		};
	};
};

const SPEC_ID = 'https://status200uploads.com/openapi.yaml';
const REQUIRED_BY_CODE = 'x-status200-required-by-code';

/** The value at a local ref ("#/components/..."). */
export function resolveRef<T = Json>(ref: string): T {
	let at: unknown = spec;
	for (const raw of ref.replace(/^#\//, '').split('/')) {
		at = (at as Json)[raw.replace(/~1/g, '/').replace(/~0/g, '~')];
		if (at === undefined) throw new Error(`unresolved ref ${ref}`);
	}
	return at as T;
}

/** An object that may be a $ref, resolved. */
export function deref<T = Json>(value: unknown): T {
	const v = value as Json;
	return (typeof v?.$ref === 'string' ? resolveRef(v.$ref) : v) as T;
}

/** The main address's operations: paths without a server of their own. */
export function v2Operations(): Array<{ method: string; path: string; op: Json; pathItem: Json }> {
	const out: Array<{ method: string; path: string; op: Json; pathItem: Json }> = [];
	for (const [path, item] of Object.entries(spec.paths)) {
		if (item.servers) continue;
		for (const method of ['get', 'post', 'delete', 'put', 'patch']) {
			if (item[method])
				out.push({ method: method.toUpperCase(), path, op: item[method] as Json, pathItem: item });
		}
	}
	return out;
}

/** The main address's operation of a method and path template. */
export function v2Operation(method: string, path: string): Json | undefined {
	return v2Operations().find((o) => o.method === method && o.path === path)?.op;
}

/** Every error code the file lists (x-error-codes) for a v2 operation, with its status. */
export function errorCodesOf(op: Json): Array<{ status: string; code: string }> {
	const out: Array<{ status: string; code: string }> = [];
	for (const [status, response] of Object.entries((op.responses ?? {}) as Json)) {
		const r = deref<Json>(response);
		for (const code of (r['x-error-codes'] as string[] | undefined) ?? [])
			out.push({ status, code });
	}
	return out;
}

/** An Ajv that knows the whole file, so a schema can be compiled from a JSON Pointer into it. */
function makeAjv(): Ajv2020 {
	const ajv = new Ajv2020({ strict: true, allowUnionTypes: true, allErrors: true });
	addFormats(ajv);
	ajv.addVocabulary([
		'x-known-values',
		'x-status200-not-used',
		'x-status200-options-by-platform',
		'example',
		'openapi',
		'info',
		'servers',
		'security',
		'tags',
		'paths',
		'components',
		'externalDocs',
		'webhooks',
		'jsonSchemaDialect',
		'x-status200-unknown-path',
	]);
	ajv.addKeyword({
		keyword: REQUIRED_BY_CODE,
		type: 'object',
		schemaType: 'object',
		validate: (schema: Record<string, string[]>, data: Json) => {
			const code = typeof data?.code === 'string' ? data.code : '(no code)';
			const need = schema[code];
			return (
				!Array.isArray(need) || need.every((k) => Object.prototype.hasOwnProperty.call(data, k))
			);
		},
	});
	ajv.addSchema({ ...spec, $id: SPEC_ID });
	return ajv;
}

const ajv = makeAjv();

/** A validator of the schema at a JSON Pointer of the file (e.g. /components/schemas/PostRequest). */
export function validatorAt(pointer: string): ValidateFunction {
	const ref = `${SPEC_ID}#${pointer}`;
	return ajv.getSchema(ref) ?? ajv.compile({ $ref: ref });
}

/** Validates data against a schema of the file; the Ajv errors as text when it does not fit. */
export function check(pointer: string, data: unknown): string {
	const validate = validatorAt(pointer);
	return validate(data) ? '' : ajv.errorsText(validate.errors);
}

/** The named examples of a response of components.responses (e.g. Published, Accepted). */
export function responseExamples(name: string): Record<string, Json> {
	const response = spec.components.responses[name] as Json;
	const content = (response.content as Json)['application/json'] as Json;
	const examples = (content.examples ?? {}) as Record<string, { value: Json }>;
	return Object.fromEntries(Object.entries(examples).map(([k, v]) => [k, v.value]));
}
