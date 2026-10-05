export const RATES_TO_NGN = Object.freeze({
  NGN: 1,
  USD: 1500,
  GBP: 1900,
  EUR: 1650
});

export const ALLOWED_CURRENCIES = Object.freeze(Object.keys(RATES_TO_NGN));
const MAX_AMOUNT_LENGTH = 50;

export function validateAmount(value) {
  if (typeof value === 'string') {
    if (value.trim() === '') {
      return { ok: false, code: 'EMPTY_AMOUNT', message: 'Enter an amount to continue.' };
    }
    if (value.length > MAX_AMOUNT_LENGTH) {
      return { ok: false, code: 'AMOUNT_TOO_LONG', message: 'That amount is too long. Enter a shorter number.' };
    }

    const amount = Number(value.trim());

    if (!Number.isFinite(amount)) {
      return { ok: false, code: 'INVALID_AMOUNT', message: 'Enter a valid number, for example 2500.' };
    }

    if (amount < 0) {
      return { ok: false, code: 'NEGATIVE_AMOUNT', message: 'Amount must be zero or greater.' };
    }

    return { ok: true, value: amount };
  }

  if (typeof value === 'number') {
    if (!Number.isFinite(value)) {
      return { ok: false, code: 'INVALID_AMOUNT', message: 'Enter a valid number, for example 2500.' };
    }

    if (value < 0) {
      return { ok: false, code: 'NEGATIVE_AMOUNT', message: 'Amount must be zero or greater.' };
    }

    if (String(value).length > MAX_AMOUNT_LENGTH) {
      return { ok: false, code: 'AMOUNT_TOO_LONG', message: 'That amount is too long. Enter a shorter number.' };
    }

    return { ok: true, value };
  }

  return {
    ok: false,
    code: 'UNEXPECTED_TYPE',
    message: 'Enter the amount as a number or numeric text.'
  };
}

export function validateCurrency(code) {
  if (typeof code !== 'string' || !Object.hasOwn(RATES_TO_NGN, code)) {
    return {
      ok: false,
      code: 'UNSUPPORTED_CURRENCY',
      message: 'That currency is not supported in this demo.'
    };
  }

  return { ok: true, value: code };
}

export function convertCurrency(amountInput, fromInput, toInput) {
  const amount = validateAmount(amountInput);
  if (!amount.ok) return amount;

  const from = validateCurrency(fromInput);
  if (!from.ok) return from;

  const to = validateCurrency(toInput);
  if (!to.ok) return to;

  const result = (amount.value * RATES_TO_NGN[from.value]) / RATES_TO_NGN[to.value];

  return {
    ok: true,
    value: Number(result.toFixed(2)),
    from: from.value,
    to: to.value
  };
}

export function safeLog(errorCode, field) {
  // Never log raw user input or internal exception details.
  console.warn('[SwiftServe]', { errorCode, field });
}
