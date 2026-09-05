def validate_bill(bill):
    errors = []

    # Check each item's calculation
    for item in bill.items:
        expected_total = item.quantity * item.unit_price

        if abs(expected_total - item.total) > 0.01:
            errors.append(
                f"Total mismatch for {item.name}: "
                f"expected {expected_total:.2f}, "
                f"got {item.total:.2f}"
            )

    # Check subtotal against item totals
    if bill.subtotal is not None:
        calculated_subtotal = sum(item.total for item in bill.items)

        if abs(calculated_subtotal - bill.subtotal) > 0.01:
            errors.append(
                f"Subtotal mismatch: "
                f"expected {calculated_subtotal:.2f}, "
                f"got {bill.subtotal:.2f}"
            )

    return errors