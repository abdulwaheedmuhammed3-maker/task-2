
# SwiftServe Error Handling Demo

A small local-only web page that converts currency using a fixed in-memory rate table and demonstrates graceful error handling.

## Run

Open index.html in a modern browser.

Run the automated tests with one command:

~~~bash
npm test
~~~

No internet connection and no live service are required.

## Fixed demo rates

These are intentionally local demo values, not live exchange rates:

- NGN = 1
- USD = 1500
- GBP = 1900
- EUR = 1650

## Failure cases

| Failure case | Example | What the user sees | What is logged |
|---|---|---|---|
| Empty input | blank | Enter an amount to continue. | EMPTY_AMOUNT |
| Whitespace-only input | spaces | Enter an amount to continue. | EMPTY_AMOUNT |
| Invalid number | abc | Enter a valid number, for example 2500. | INVALID_AMOUNT |
| Negative amount | -50 | Amount must be zero or greater. | NEGATIVE_AMOUNT |
| Very long input | 51+ characters | That amount is too long. Enter a shorter number. | AMOUNT_TOO_LONG |
| Unexpected type | object, array, null, boolean | Enter the amount as a number or numeric text. | UNEXPECTED_TYPE |
| Unsupported currency | JPY | That currency is not supported in this demo. | UNSUPPORTED_CURRENCY |
| Malformed JSON (test-level example) | invalid JSON payload | Request could not be understood. | INVALID_JSON |

## Error-handling approach

The page never exposes stack traces, internal exceptions, file paths, or implementation details to the user.

Instead, errors are converted into safe, actionable messages such as:

> Enter a valid number, for example 2500.

The logger records only a short error code and field name. It does not record raw user input or personal data.

## Tests

The test suite covers:
1. Valid conversion
2. Empty input
3. Whitespace-only input
4. Invalid numeric input
5. Negative input
6. Very long input
7. Unexpected JavaScript types
8. Unsupported currency
9. Safe logging

Run everything with:

~~~bash
npm test
~~~
