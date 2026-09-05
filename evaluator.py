import json
from pathlib import Path


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compare_fields(predicted, actual):
    results = {}

    fields = [
        "vendor_name",
        "invoice_number",
        "date",
        "subtotal",
        "tax",
        "discount",
        "total",
    ]

    # Compare main bill fields
    for field in fields:
        predicted_value = predicted.get(field)
        actual_value = actual.get(field)

        results[field] = predicted_value == actual_value

    # Compare line items
    predicted_items = predicted.get("items", [])
    actual_items = actual.get("items", [])

    results["items_count"] = len(predicted_items) == len(actual_items)

    # Compare each item
    for index, actual_item in enumerate(actual_items):

        if index >= len(predicted_items):
            break

        predicted_item = predicted_items[index]

        item_name = f"item_{index + 1}"

        results[f"{item_name}_name"] = (
            predicted_item.get("name")
            == actual_item.get("name")
        )

        results[f"{item_name}_quantity"] = (
            predicted_item.get("quantity")
            == actual_item.get("quantity")
        )

        results[f"{item_name}_unit_price"] = (
            predicted_item.get("unit_price")
            == actual_item.get("unit_price")
        )

        results[f"{item_name}_total"] = (
            predicted_item.get("total")
            == actual_item.get("total")
        )

    return results


def calculate_accuracy(results):
    total_fields = len(results)
    correct_fields = sum(results.values())

    if total_fields == 0:
        return 0.0

    return (correct_fields / total_fields) * 100


def evaluate_bill(predicted_path, ground_truth_path):
    predicted = load_json(predicted_path)
    actual = load_json(ground_truth_path)

    results = compare_fields(predicted, actual)
    accuracy = calculate_accuracy(results)

    return results, accuracy


# File paths
predicted_path = Path("outputs/test_bill.json")
ground_truth_path = Path("evaluation/ground_truth/test_bill.json")


# Run evaluation
results, accuracy = evaluate_bill(
    predicted_path,
    ground_truth_path
)


# Display results
print("\nField-level evaluation:")

for field, correct in results.items():
    status = "PASS" if correct else "FAIL"
    print(f"{field}: {status}")

print(f"\nField Accuracy: {accuracy:.2f}%")