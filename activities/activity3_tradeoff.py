"""Activity 3: quality trade-off (readability vs. speed vs. correctness)."""
from time import perf_counter


def calculate_total(items):
    # Clear O(n) implementation: readable, correct, fast enough.
    return sum(item["price"] * item["qty"] for item in items)


def calculate_total_loop(items):
    # Equivalent explicit loop: more verbose, same O(n).
    total = 0
    for item in items:
        total += item["price"] * item["qty"]
    return total


if __name__ == "__main__":
    items = [{"price": 10, "qty": 2}] * 200_000
    for fn in (calculate_total, calculate_total_loop):
        t = perf_counter()
        result = fn(items)
        print(f"{fn.__name__:22} result={result} time={perf_counter() - t:.4f}s")
