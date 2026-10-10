"""Pure business logic: no print(), no I/O, no formatting."""
from dataclasses import dataclass
from typing import Iterable

from .exceptions import InvalidItemError, InvalidRateError


@dataclass(frozen=True)
class LineItem:
    description: str
    unit_price: float
    qty: int = 1

    def __post_init__(self):
        if self.unit_price < 0:
            raise InvalidItemError("unit_price must be >= 0")
        if self.qty <= 0:
            raise InvalidItemError("qty must be > 0")

    @property
    def amount(self) -> float:
        return self.unit_price * self.qty


@dataclass(frozen=True)
class InvoiceTotals:
    subtotal: float
    discount: float
    tax: float
    total: float


def _check_rate(name: str, rate: float) -> None:
    if not 0 <= rate <= 1:
        raise InvalidRateError(f"{name} must be between 0 and 1, got {rate}")


def subtotal(items: Iterable[LineItem]) -> float:
    return sum(i.amount for i in items)


def discount_amount(base: float, discount_rate: float) -> float:
    _check_rate("discount_rate", discount_rate)
    return base * discount_rate


def tax_amount(taxable: float, tax_rate: float) -> float:
    _check_rate("tax_rate", tax_rate)
    return taxable * tax_rate


def compute_totals(items, tax_rate=0.0, discount_rate=0.0) -> InvoiceTotals:
    """Tax is charged on the discounted subtotal."""
    base = subtotal(items)
    disc = discount_amount(base, discount_rate)
    tax = tax_amount(base - disc, tax_rate)
    return InvoiceTotals(base, disc, tax, base - disc + tax)
