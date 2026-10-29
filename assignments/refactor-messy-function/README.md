# Refactor a Messy Function Without Changing Behaviour

This assignment demonstrates a behaviour-preserving refactor of a long Python function that validates a shopping cart and calculates discounts, tax, shipping, and a customer-facing summary.

## Run the tests

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Test-first approach

The original implementation was committed first. The test suite was then committed **before any refactor** and run against that original implementation. It covers normal pricing, defaults and whitespace, discount precedence, coupon threshold boundaries, empty and invalid coupons, regional tax/shipping, malformed carts/items, and floating-point rounding behaviour.

## Refactor notes

The original `process_order` function mixes input validation, line-item normalization, discount selection, tax calculation, shipping calculation, and response formatting. The refactor extracts these responsibilities into smaller private helper functions while preserving the public function signature, return keys, calculation order, and existing edge-case behaviour.

The refactor is split into separate commits. The test suite is run after each refactoring step.

## Trade-offs

This is a teaching example, not a production checkout engine. It uses floats and Python's built-in `round`, so real financial software should use `Decimal` and an explicit rounding policy. Tax and shipping rules are simplified examples.
