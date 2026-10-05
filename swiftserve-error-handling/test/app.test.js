import test from 'node:test';
import assert from 'node:assert/strict';
import { convertCurrency, validateAmount, validateCurrency, safeLog } from '../app.js';

test('valid conversion succeeds', () => {
  const result = convertCurrency('3000', 'NGN', 'USD');
  assert.equal(result.ok, true);
  assert.equal(result.value, 2);
  assert.equal(result.to, 'USD');
});

test('empty input fails gracefully', () => {
  const result = validateAmount('');
  assert.equal(result.ok, false);
  assert.equal(result.code, 'EMPTY_AMOUNT');
});

test('whitespace-only input fails gracefully', () => {
  const result = validateAmount('   ');
  assert.equal(result.ok, false);
  assert.equal(result.code, 'EMPTY_AMOUNT');
});

test('invalid numeric input fails gracefully', () => {
  const result = validateAmount('abc');
  assert.equal(result.ok, false);
  assert.equal(result.code, 'INVALID_AMOUNT');
});

test('negative input fails gracefully', () => {
  const result = validateAmount('-50');
  assert.equal(result.ok, false);
  assert.equal(result.code, 'NEGATIVE_AMOUNT');
});

test('very long input fails gracefully', () => {
  const result = validateAmount('9'.repeat(51));
  assert.equal(result.ok, false);
  assert.equal(result.code, 'AMOUNT_TOO_LONG');
});

test('unexpected types fail gracefully', () => {
  for (const value of [null, undefined, {}, [], true, false]) {
    const result = validateAmount(value);
    assert.equal(result.ok, false);
    assert.equal(result.code, 'UNEXPECTED_TYPE');
  }
});

test('unsupported currency fails gracefully', () => {
  const result = validateCurrency('JPY');
  assert.equal(result.ok, false);
  assert.equal(result.code, 'UNSUPPORTED_CURRENCY');
});

test('safe logger does not log raw user input or internals', () => {
  const originalWarn = console.warn;
  const captured = [];
  console.warn = function () {
    captured.push(Array.from(arguments));
  };

  safeLog('INVALID_AMOUNT', 'amount');

  console.warn = originalWarn;

  assert.equal(captured.length, 1);
  assert.equal(captured[0][0], '[SwiftServe]');
  assert.deepEqual(captured[0][1], { errorCode: 'INVALID_AMOUNT', field: 'amount' });
});
