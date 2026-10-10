import json
import pytest

from invoice_app.calculator import LineItem, compute_totals, subtotal
from invoice_app.exceptions import InvalidItemError, InvalidRateError
from invoice_app.service import InvoiceService
from activities.activity1_separation import calculate_fee, invoice_text
from activities.activity2_serializer import invoice_json

ITEMS = [LineItem("Tuition", 1000), LineItem("Lab", 250, 2)]  # subtotal 1500


def test_activity1_fee_and_text():
    assert calculate_fee(12000, 3) == 12150
    assert invoice_text("Ali", 12150) == "Ali: PKR 12150.00"


def test_activity2_json():
    assert json.loads(invoice_json("Ali", 12150)) == {"student": "Ali", "amount": 12150}


def test_subtotal():
    assert subtotal(ITEMS) == 1500


def test_discount():  # Rule 1
    assert compute_totals(ITEMS, discount_rate=0.1).total == pytest.approx(1350)


def test_tax_on_discounted_amount():  # Rule 2
    t = compute_totals(ITEMS, tax_rate=0.05, discount_rate=0.1)
    assert t.tax == pytest.approx(67.5)
    assert t.total == pytest.approx(1417.5)


@pytest.mark.parametrize("rate", [-0.01, 1.01])
def test_rate_out_of_range_rejected(rate):
    with pytest.raises(InvalidRateError):
        compute_totals(ITEMS, tax_rate=rate)


@pytest.mark.parametrize("rate", [0, 1])
def test_rate_boundaries_allowed(rate):
    compute_totals(ITEMS, discount_rate=rate)


def test_invalid_items():
    with pytest.raises(InvalidItemError):
        LineItem("x", -1)
    with pytest.raises(InvalidItemError):
        LineItem("x", 10, 0)


def test_empty_invoice_is_zero():
    assert InvoiceService().final_total([]) == 0


def test_text_and_json_share_same_totals():
    svc = InvoiceService(0.05, 0.1)
    data = json.loads(svc.render("Ali", ITEMS, "json"))
    assert data["total"] == pytest.approx(svc.final_total(ITEMS))
    assert "1,417.50" in svc.render("Ali", ITEMS, "text")


def test_unknown_format():
    with pytest.raises(ValueError):
        InvoiceService().render("Ali", ITEMS, "xml")
