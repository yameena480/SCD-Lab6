# CSE325 – Lab 06: Design, Coding, Testing, Reuse & Quality

**Scenario:** A university fee system generates invoices in text and JSON without duplicating fee-calculation logic.
**CLOs:** CLO-2, CLO-5, CLO-6

## Setup / Run / Test
```
python -m venv .venv && .\.venv\Scripts\activate
python -m pip install pytest coverage
python -m activities.activity1_separation   # Activity 1
python -m activities.activity2_serializer   # Activity 2
python -m activities.activity3_tradeoff     # Activity 3
python -m invoice_app.main                  # Activity 4 demo
python -m pytest -q                         # 19 tests
python -m coverage run -m pytest && python -m coverage report
```

## Architecture (Activity 4)
```
main.py (I/O shell: only place that prints)
   |
InvoiceService  --->  calculator.py (pure rules: subtotal, discount, tax)
   |
   +--->  formatters.py (to_text / to_json, reuses stdlib json)
```
Calculation, formatting and I/O are three separate layers; text and JSON both reuse the same `compute_totals`.

## Business rules (tested)
| # | Rule |
|---|------|
| 1 | Discount = subtotal x discount_rate |
| 2 | Tax is charged on the *discounted* subtotal |
| 3 | Rates must be within 0..1 (else `InvalidRateError`) |
| 4 | unit_price >= 0 and qty > 0 (else `InvalidItemError`) |
| 5 | Empty invoice totals 0 |

## Graded Lab Tasks
1. **Notification formatter** – `notify_app/formatter.py`: `EmailFormatter` and `SmsFormatter` share the `NotificationFormatter` interface; `notify()` accepts any formatter.
2. **Tests for >= 4 business rules** – `tests/test_invoice.py` (discount, tax-on-discounted, rate bounds, item validation, empty invoice) and `tests/test_notify.py` (SMS 160-char limit, required fields).
3. **Separate calculation, formatting, I/O** – `calculator.py` / `formatters.py` / `main.py`; in `notify`, I/O is injected via `sender=` so tests capture output instead of printing.
4. **Quality trade-off** – `calculate_total` uses a generator expression with `sum()` rather than a manual loop. Measured: ~0.0084s vs ~0.0088s for 200k items, so the clearer version costs nothing. A hand-optimised version would add complexity for no measured gain, so readability wins.
5. **Reusable standard-library feature** – `json.dumps` (serialisation) and `dataclasses.asdict` / `abc.ABC`, instead of hand-building JSON strings.

## Viva answers
- **Why separate I/O from business logic?** Logic can be unit-tested without capturing output, reused with different front ends (text, JSON, web), and changed independently.
- **What does reuse mean beyond copy-paste?** Calling one tested implementation from many places (a shared function, module, or library) so a fix happens once.
- **What is a quality attribute?** A non-functional property such as maintainability, performance, reliability, or security that shapes design choices.
- **Why can more abstraction hurt readability?** Extra layers and indirection make readers jump between files to follow simple behaviour; abstract only where change is likely.

## Suggested Git commits
```
git init
git add activities/activity1_separation.py && git commit -m "feat: separate fee calculation from invoice text"
git add activities/activity2_serializer.py  && git commit -m "feat: add JSON invoice using stdlib json"
git add activities/activity3_tradeoff.py    && git commit -m "docs: add quality trade-off benchmark"
git add invoice_app && git commit -m "feat: add InvoiceService with discount and tax"
git add notify_app  && git commit -m "feat: add email/SMS notification formatters"
git add tests pytest.ini README.md && git commit -m "test: cover business rules; add README"
```

## Independent extension (example)
*Requirement:* add a late-fee rule (PKR 50/day) as an extra `LineItem`. Only `calculator.py` changes (new helper `late_fee_item(days)`); add a test, commit separately.
