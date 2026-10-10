from . import calculator, formatters


class InvoiceService:
    FORMATS = {"text": formatters.to_text, "json": formatters.to_json}

    def __init__(self, tax_rate=0.0, discount_rate=0.0):
        self.tax_rate = tax_rate
        self.discount_rate = discount_rate

    def final_total(self, items) -> float:
        return self.totals(items).total

    def totals(self, items):
        return calculator.compute_totals(items, self.tax_rate, self.discount_rate)

    def render(self, student, items, fmt="text") -> str:
        try:
            formatter = self.FORMATS[fmt]
        except KeyError:
            raise ValueError(f"Unsupported format: {fmt}") from None
        return formatter(student, self.totals(items))
