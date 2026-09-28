import { InvalidInput } from './input';

/**
 * A date and time with no time zone: what n8n's date picker stores ("2026-10-01T09:00:00"), and what
 * people type ("2026-10-01 09:00", "2026-10-01"). The API refuses these (400 scheduled_for_invalid,
 * reason no_time_zone), so the node reads them in the workflow's time zone.
 */
const ZONELESS = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{1,9}))?)?)?$/;

interface WallTime {
	year: number;
	month: number;
	day: number;
	hour: number;
	minute: number;
	second: number;
	millisecond: number;
}

/** The zone's offset from UTC at an instant, in minutes. */
function offsetMinutesAt(utcMs: number, timeZone: string): number {
	const parts = new Intl.DateTimeFormat('en-US', {
		timeZone,
		hourCycle: 'h23',
		year: 'numeric',
		month: '2-digit',
		day: '2-digit',
		hour: '2-digit',
		minute: '2-digit',
		second: '2-digit',
	}).formatToParts(new Date(utcMs));
	const get = (type: string): number => Number(parts.find((p) => p.type === type)?.value);
	const wallAsUtc = Date.UTC(
		get('year'),
		get('month') - 1,
		get('day'),
		get('hour'),
		get('minute'),
		get('second'),
	);
	return Math.round((wallAsUtc - Math.floor(utcMs / 1000) * 1000) / 60000);
}

const DAY_MS = 24 * 60 * 60 * 1000;

/**
 * The instant a wall-clock time names in a zone. The zone's offsets a day before and a day after are
 * the candidates; a candidate is right when the zone has that offset at the instant it gives. A time
 * that happens twice (the clock goes back) is the first of the two; a time the clock skips (it goes
 * forward) is read with the offset before the change, so it lands just after the change, as calendars
 * do.
 */
export function wallTimeToUtc(wall: WallTime, timeZone: string): Date {
	const wallMs = Date.UTC(
		wall.year,
		wall.month - 1,
		wall.day,
		wall.hour,
		wall.minute,
		wall.second,
		wall.millisecond,
	);
	const before = offsetMinutesAt(wallMs - DAY_MS, timeZone);
	const after = offsetMinutesAt(wallMs + DAY_MS, timeZone);
	const fits = [before, after]
		.map((offset) => wallMs - offset * 60000)
		.filter((utc) => wallMs - utc === offsetMinutesAt(utc, timeZone) * 60000);
	return new Date(fits.length > 0 ? Math.min(...fits) : wallMs - before * 60000);
}

function validZone(timeZone: string): boolean {
	try {
		new Intl.DateTimeFormat('en-US', { timeZone });
		return true;
	} catch {
		return false;
	}
}

function parseZoneless(text: string): WallTime | null {
	const m = ZONELESS.exec(text);
	if (!m) return null;
	const wall: WallTime = {
		year: Number(m[1]),
		month: Number(m[2]),
		day: Number(m[3]),
		hour: m[4] === undefined ? 0 : Number(m[4]),
		minute: m[5] === undefined ? 0 : Number(m[5]),
		second: m[6] === undefined ? 0 : Number(m[6]),
		millisecond: m[7] === undefined ? 0 : Number(m[7].slice(0, 3).padEnd(3, '0')),
	};
	const day = new Date(Date.UTC(wall.year, wall.month - 1, wall.day));
	const real =
		wall.month >= 1 &&
		wall.month <= 12 &&
		day.getUTCDate() === wall.day &&
		day.getUTCMonth() === wall.month - 1 &&
		wall.hour <= 23 &&
		wall.minute <= 59 &&
		wall.second <= 59;
	return real ? wall : null;
}

/**
 * post.scheduledFor from the node's Scheduled For value:
 *   - a date and time without a zone is read in the workflow's time zone and sent in UTC;
 *   - a value with a zone, a Unix time, or any other text is sent as it is (the API reads it, or
 *     answers 400 scheduled_for_invalid with its reason);
 *   - a Luxon DateTime or a Date (from an expression) is sent as ISO 8601 with its offset.
 */
export function scheduledForValue(value: unknown, timeZone: string): string | number {
	if (typeof value === 'number' && Number.isFinite(value)) return value;
	if (value instanceof Date) {
		if (Number.isNaN(value.getTime())) {
			throw new InvalidInput(
				'Scheduled For is not a valid date',
				'Pick a date and time, or send an ISO 8601 time with a time zone',
			);
		}
		return value.toISOString();
	}
	if (
		value !== null &&
		typeof value === 'object' &&
		typeof (value as { toISO?: unknown }).toISO === 'function'
	) {
		const iso = (value as { toISO: () => string | null }).toISO();
		if (iso) return iso;
		throw new InvalidInput(
			'Scheduled For is not a valid date',
			'Pick a date and time, or send an ISO 8601 time with a time zone',
		);
	}
	const text = typeof value === 'string' ? value.trim() : '';
	if (text === '') {
		throw new InvalidInput('Scheduled For is empty', 'Pick a date and time, or set When to Now');
	}
	const wall = parseZoneless(text);
	if (!wall) return text;
	if (!validZone(timeZone)) {
		throw new InvalidInput(
			`The workflow's time zone "${timeZone}" is not known`,
			'Set a time zone in the workflow settings, or add one to Scheduled For (for example 2026-10-01T09:00:00Z)',
		);
	}
	return wallTimeToUtc(wall, timeZone).toISOString();
}
