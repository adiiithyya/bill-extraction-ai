import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import Bill


load_dotenv()

client = genai.Client()


def extract_bill(image_path):
    suffix = Path(image_path).suffix.lower()

    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }

    mime_type = mime_types.get(suffix)

    if mime_type is None:
        raise ValueError(f"Unsupported image format: {suffix}")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=mime_type,
                    ),
                    """
                    Look at this bill carefully.

                    Extract the following information:
                    - Vendor name
                    - Bill/invoice number
                    - Date
                    - All purchased items
                    - Quantity of each item
                    - Unit price of each item
                    - Total price of each item
                    - Subtotal
                    - Tax
                    - Discount
                    - Final total

                    If a field is not present on the bill, return null.
                    Do not guess information.
                    """
                ],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Bill,
                },
            )

            return Bill.model_validate_json(response.text)

        except Exception as e:
            if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < 2:
                print(
                    f"Gemini is busy. Retrying... ({attempt + 1}/2)"
                )
                time.sleep(3)
            else:
                raise