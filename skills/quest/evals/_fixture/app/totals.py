"""Invoice totals for the shop."""


def invoice_total(items):
    """Return the total of (price, quantity) pairs, rounded to cents."""
    return round(sum(price * quantity for price, quantity in items), 2)
