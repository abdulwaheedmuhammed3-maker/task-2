# Refactor a Messy Function Without Changing Behaviour

This assignment demonstrates a behaviour-preserving refactor of a long Python function that validates a shopping cart and calculates discounts, tax, shipping, and a customer-facing summary.

## Run the tests

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Test-first approach

The original implementation was committed first. The test suite was committed **before any refactor** and run against that original implementation. It covers normal pricing, defaults and whitespace, discount precedence, coupon threshold boundaries, empty and invalid coupons, regional tax/shipping, malformed carts/items, and floating-point rounding behaviour.

## What was split out and why

- `_normalize_items`: validates the cart and each item, trims names, applies the default quantity, and computes line totals. This keeps input handling separate from pricing policy.
- `_get_discount_rate`: applies customer discounts and coupon rules in one place, including the existing non-stacking behaviour and coupon threshold.
- `_calculate_tax_and_shipping`: calculates taxable amount, tax, shipping and final total. Keeping these calculations together makes the pricing rules easier to inspect.
- `process_order`: now coordinates the helpers and assembles the same public result dictionary.

The refactor is split into two distinct commits. The full test suite was run after each refactoring step; all 15 tests passed each time. The function signature, return keys, calculation order, and edge-case behaviour remain unchanged.

## Trade-offs

This is a teaching example, not a production checkout engine. It uses floats and Python's built-in `round`, so real financial software should use `Decimal` and an explicit rounding policy. Tax and shipping rules are simplified examples.
