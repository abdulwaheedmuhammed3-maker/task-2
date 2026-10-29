def _normalize_items(items):
    """Validate cart input and return normalized lines plus subtotal."""
    if not isinstance(items, list) or len(items) == 0:
        raise ValueError("items must be a non-empty list")

    subtotal = 0
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("each item must be a dictionary")
        name = item.get("name")
        price = item.get("price")
        quantity = item.get("quantity", 1)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("item name is required")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise ValueError("quantity must be a positive integer")
        line_total = round(price * quantity, 2)
        subtotal += line_total
        normalized.append({"name": name.strip(), "quantity": quantity, "line_total": line_total})

    return normalized, round(subtotal, 2)


def process_order(items, customer_type="regular", coupon=None, region="local"):
    """Validate a cart and return a priced order summary."""
    normalized, subtotal = _normalize_items(items)

    if customer_type not in ("regular", "member", "staff"):
        raise ValueError("unknown customer type")
    discount_rate = 0
    if customer_type == "member":
        discount_rate = 0.05
    elif customer_type == "staff":
        discount_rate = 0.10

    if coupon is not None:
        if not isinstance(coupon, str):
            raise ValueError("coupon must be text")
        code = coupon.strip().upper()
        if code == "SAVE10":
            discount_rate = max(discount_rate, 0.10)
        elif code == "SAVE20" and subtotal >= 100:
            discount_rate = max(discount_rate, 0.20)
        elif code != "":
            raise ValueError("invalid coupon")

    discount = round(subtotal * discount_rate, 2)
    taxable = round(subtotal - discount, 2)
    tax_rate = 0.075 if region in ("local", "nearby") else 0.12
    tax = round(taxable * tax_rate, 2)

    if region not in ("local", "nearby", "remote"):
        raise ValueError("unknown shipping region")
    if region == "local":
        shipping = 0 if subtotal >= 50 else 5
    elif region == "nearby":
        shipping = 8
    else:
        shipping = 15

    total = round(taxable + tax + shipping, 2)
    return {
        "items": normalized,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "shipping": shipping,
        "total": total,
        "currency": "NGN",
        "message": f"{len(normalized)} item type(s) processed",
    }
