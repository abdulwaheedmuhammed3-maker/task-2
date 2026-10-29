import pytest

from messy_function import process_order


def test_regular_order_applies_local_tax_and_free_shipping_threshold():
    result = process_order([{"name": "Notebook", "price": 50, "quantity": 1}])
    assert result["subtotal"] == 50
    assert result["discount"] == 0
    assert result["tax"] == 3.75
    assert result["shipping"] == 0
    assert result["total"] == 53.75


def test_missing_quantity_defaults_to_one_and_trims_name():
    result = process_order([{"name": "  Pen ", "price": 10}])
    assert result["items"] == [{"name": "Pen", "quantity": 1, "line_total": 10}]
    assert result["message"] == "1 item type(s) processed"


def test_member_discount_and_coupon_do_not_stack():
    result = process_order([{"name": "Book", "price": 100}], customer_type="member", coupon="SAVE10")
    assert result["discount"] == 10
    assert result["tax"] == 6.75


def test_save20_requires_subtotal_of_at_least_100():
    with pytest.raises(ValueError, match="invalid coupon"):
        process_order([{"name": "A", "price": 99.99}], coupon="SAVE20")
    high = process_order([{"name": "A", "price": 100}], coupon=" save20 ")
    assert high["discount"] == 20


def test_empty_coupon_is_accepted_but_unknown_coupon_is_rejected():
    assert process_order([{"name": "A", "price": 10}], coupon="")["discount"] == 0
    with pytest.raises(ValueError, match="invalid coupon"):
        process_order([{"name": "A", "price": 10}], coupon="NOPE")


def test_remote_region_uses_higher_tax_and_shipping():
    result = process_order([{"name": "Cable", "price": 20}], region="remote")
    assert result["tax"] == 2.4
    assert result["shipping"] == 15
    assert result["total"] == 37.4


@pytest.mark.parametrize("items", [[], None, "not a list"])
def test_cart_must_be_a_non_empty_list(items):
    with pytest.raises(ValueError, match="non-empty list"):
        process_order(items)


@pytest.mark.parametrize("item", [
    {"name": " ", "price": 2},
    {"name": "Pen", "price": -1},
    {"name": "Pen", "price": True},
    {"name": "Pen", "price": 2, "quantity": 0},
    {"name": "Pen", "price": 2, "quantity": True},
])
def test_invalid_item_fields_are_rejected(item):
    with pytest.raises(ValueError):
        process_order([item])


def test_rounding_is_applied_to_each_line_before_subtotal():
    result = process_order([
        {"name": "A", "price": 1.005},
        {"name": "B", "price": 1.005},
    ])
    assert result["subtotal"] == 2.0  # Python float rounding behaviour is intentional here
