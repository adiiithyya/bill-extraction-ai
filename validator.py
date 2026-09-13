def validate_bill(bill):
    errors = []

    # Check that extracted item values are valid
    for item in bill.items:
        if item.quantity <= 0:
            errors.append(
                f"Invalid quantity for {item.name}: {item.quantity}"
            )

        if item.unit_price < 0:
            errors.append(
                f"Invalid unit price for {item.name}: {item.unit_price:.2f}"
            )

        if item.total < 0:
            errors.append(
                f"Invalid total for {item.name}: {item.total:.2f}"
            )

    # If subtotal is explicitly available,
    # compare it with the sum of extracted item totals.
    if bill.subtotal is not None:
        calculated_subtotal = sum(
            item.total for item in bill.items
        )

        if abs(calculated_subtotal - bill.subtotal) > 0.02:
            errors.append(
                f"Subtotal mismatch: "
                f"expected {calculated_subtotal:.2f}, "
                f"got {bill.subtotal:.2f}"
            )

    # Validate the final total when the invoice structure
    # provides enough information to do so.
    if bill.total is not None and bill.subtotal is not None:

        if bill.tax is not None:
            expected_total = bill.subtotal + bill.tax

            if bill.discount is not None:
                expected_total -= bill.discount

            # Some invoices already include tax inside the subtotal.
            # Therefore, accept either representation.
            if (
                abs(bill.total - expected_total) > 0.02
                and abs(bill.total - bill.subtotal) > 0.02
            ):
                errors.append(
                    f"Total mismatch: "
                    f"expected approximately {expected_total:.2f} "
                    f"or subtotal-inclusive total {bill.subtotal:.2f}, "
                    f"got {bill.total:.2f}"
                )

        else:
            if bill.discount is not None:
                expected_total = bill.subtotal - bill.discount

                if abs(bill.total - expected_total) > 0.02:
                    errors.append(
                        f"Total mismatch: "
                        f"expected {expected_total:.2f}, "
                        f"got {bill.total:.2f}"
                    )

    return errors