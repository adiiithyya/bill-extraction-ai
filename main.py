import sys
from pathlib import Path

from extractor import extract_bill
from validator import validate_bill

sys.stdout.reconfigure(encoding="utf-8")


bill_folder = Path("bills")
output_folder = Path("outputs")

output_folder.mkdir(exist_ok=True)


supported_extensions = {".jpg", ".jpeg", ".png"}

for image_path in bill_folder.iterdir():
    if image_path.suffix.lower() not in supported_extensions:
        continue
        
    print(f"\nProcessing: {image_path.name}")

    try:
    	bill = extract_bill(image_path)

    except Exception as e:
    	print(f"Extraction failed for {image_path.name}: {e}")
    	print("Skipping this bill and continuing...\n")
    	continue

    output_path = output_folder / f"{image_path.stem}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(bill.model_dump_json(indent=2))

    print(f"Saved result to: {output_path}")

errors = validate_bill(bill)

if errors:
    print("\nValidation errors:")
    for error in errors:
        print(f"- {error}")
else:
    print("\nValidation successful!")

    
    print(f"Vendor: {bill.vendor_name}")
    print(f"Number of items: {len(bill.items)}")
    print(f"Subtotal: {bill.subtotal}")
    print(f"Total: {bill.total}")