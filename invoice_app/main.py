"""Imperative shell: the only place that prints."""
from .calculator import LineItem
from .service import InvoiceService


def main():
    items = [LineItem("Tuition", 12000), LineItem("Lab fee", 1500, 2)]
    svc = InvoiceService(tax_rate=0.05, discount_rate=0.10)
    print(svc.render("Ali", items, "text"))
    print(svc.render("Ali", items, "json"))


if __name__ == "__main__":
    main()
