"""Activity 1: separate calculation from output."""


def calculate_fee(base, late_days):
    penalty = late_days * 50
    return base + penalty


def invoice_text(student, amount):
    return f"{student}: PKR {amount:.2f}"


if __name__ == "__main__":
    amount = calculate_fee(12000, 3)
    print(invoice_text("Ali", amount))
