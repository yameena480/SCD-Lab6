"""Activity 2: reuse the standard-library json module."""
import json


def invoice_json(student, amount):
    return json.dumps({"student": student, "amount": amount})


if __name__ == "__main__":
    print(invoice_json("Ali", 12150))
