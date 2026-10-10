"""Presentation only. Reuses `json` from the standard library."""
import json
from dataclasses import asdict


def to_text(student: str, totals) -> str:
    return "\n".join([
        f"Invoice for {student}",
        f"Subtotal : PKR {totals.subtotal:,.2f}",
        f"Discount : PKR {totals.discount:,.2f}",
        f"Tax      : PKR {totals.tax:,.2f}",
        f"TOTAL    : PKR {totals.total:,.2f}",
    ])


def to_json(student: str, totals) -> str:
    return json.dumps({"student": student, **asdict(totals)}, indent=2)
