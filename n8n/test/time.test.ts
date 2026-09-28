import { describe, expect, it } from 'vitest';
import { InvalidInput } from '../nodes/Status200Uploads/shared/input';
import { scheduledForValue, wallTimeToUtc } from '../nodes/Status200Uploads/shared/time';

describe('scheduledForValue: a time without a zone is read in the workflow time zone', () => {
	it('what the date picker stores', () => {
		expect(scheduledForValue('2026-10-01T09:00:00', 'Europe/Berlin')).toBe(
			'2026-10-01T07:00:00.000Z',
		);
		expect(scheduledForValue('2026-10-01T09:00:00', 'America/New_York')).toBe(
			'2026-10-01T13:00:00.000Z',
		);
		expect(scheduledForValue('2026-10-01T09:00:00', 'Asia/Kolkata')).toBe(
			'2026-10-01T03:30:00.000Z',
		);
		expect(scheduledForValue('2026-10-01T09:00:00', 'UTC')).toBe('2026-10-01T09:00:00.000Z');
	});

	it('what people type: a space, no seconds, fractions, a date only', () => {
		expect(scheduledForValue('2026-12-24 18:30', 'Europe/London')).toBe('2026-12-24T18:30:00.000Z');
		expect(scheduledForValue('2026-12-24T18:30:15.250', 'Europe/London')).toBe(
			'2026-12-24T18:30:15.250Z',
		);
		expect(scheduledForValue('2026-12-24', 'Europe/Berlin')).toBe('2026-12-23T23:00:00.000Z');
	});

	it('clock changes: a time that happens twice is the first; a skipped time lands after the change', () => {
		// Berlin goes back from 03:00 +02:00 to 02:00 +01:00 on 2026-10-25: 02:30 happens twice.
		expect(scheduledForValue('2026-10-25T02:30:00', 'Europe/Berlin')).toBe(
			'2026-10-25T00:30:00.000Z',
		);
		// Berlin jumps from 02:00 +01:00 to 03:00 +02:00 on 2026-03-29: 02:30 does not exist.
		expect(scheduledForValue('2026-03-29T02:30:00', 'Europe/Berlin')).toBe(
			'2026-03-29T01:30:00.000Z',
		);
		// New York: 2026-03-08 02:30 does not exist; 2026-11-01 01:30 happens twice.
		expect(scheduledForValue('2026-03-08T02:30:00', 'America/New_York')).toBe(
			'2026-03-08T07:30:00.000Z',
		);
		expect(scheduledForValue('2026-11-01T01:30:00', 'America/New_York')).toBe(
			'2026-11-01T05:30:00.000Z',
		);
	});
});

describe('scheduledForValue: everything else is sent as it is', () => {
	it('a time with a zone', () => {
		expect(scheduledForValue('2026-10-01T09:00:00Z', 'Europe/Berlin')).toBe('2026-10-01T09:00:00Z');
		expect(scheduledForValue('2026-10-01T09:00:00+02:00', 'UTC')).toBe('2026-10-01T09:00:00+02:00');
		expect(scheduledForValue(' Wed, 30 Sep 2026 10:00:00 GMT ', 'UTC')).toBe(
			'Wed, 30 Sep 2026 10:00:00 GMT',
		);
	});

	it('a Unix time, and text the API reads or refuses itself', () => {
		expect(scheduledForValue(1790000000, 'UTC')).toBe(1790000000);
		expect(scheduledForValue('1790000000', 'UTC')).toBe('1790000000');
		expect(scheduledForValue('01/10/2026', 'UTC')).toBe('01/10/2026');
		expect(scheduledForValue('2026-02-30T10:00:00', 'UTC')).toBe('2026-02-30T10:00:00');
	});

	it('a Luxon DateTime or a Date from an expression', () => {
		const luxonLike = { toISO: () => '2026-10-01T09:00:00.000+02:00' };
		expect(scheduledForValue(luxonLike, 'UTC')).toBe('2026-10-01T09:00:00.000+02:00');
		expect(scheduledForValue(new Date('2026-10-01T07:00:00Z'), 'UTC')).toBe(
			'2026-10-01T07:00:00.000Z',
		);
	});
});

describe('scheduledForValue: what cannot be sent', () => {
	it('an empty value, an invalid date, an unknown time zone', () => {
		expect(() => scheduledForValue('', 'UTC')).toThrow(InvalidInput);
		expect(() => scheduledForValue(undefined, 'UTC')).toThrow(InvalidInput);
		expect(() => scheduledForValue(new Date('nope'), 'UTC')).toThrow(InvalidInput);
		expect(() => scheduledForValue({ toISO: () => null }, 'UTC')).toThrow(InvalidInput);
		expect(() => scheduledForValue('2026-10-01T09:00:00', 'Mars/Olympus_Mons')).toThrow(
			/time zone/,
		);
	});
});

describe('wallTimeToUtc', () => {
	it('keeps milliseconds', () => {
		const d = wallTimeToUtc(
			{ year: 2026, month: 7, day: 1, hour: 12, minute: 0, second: 0, millisecond: 5 },
			'Australia/Sydney',
		);
		expect(d.toISOString()).toBe('2026-07-01T02:00:00.005Z');
	});
});
