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

    for attempt in range(2):
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

                    Only extract values that are explicitly printed on the bill.

                    If a field is not explicitly shown, return null.
                    Do not calculate, derive, or infer missing fields.

                    For the date, carefully inspect the invoice header.
                    Check fields labeled Invoice Date, Invoice Dt, Date,
                    or similar. Extract the date exactly as printed.

                    For the totals section:
                    - Extract Subtotal only when explicitly labeled Subtotal.
                    - Do not treat Taxable Value as Subtotal.
                    - Extract Tax only when tax is explicitly shown.
                    - If CGST and SGST are both explicitly shown,
                      return their combined amount as tax.
                    - Extract Discount only when explicitly shown.
                    - Extract Total only from the explicitly labeled final total.

                    Pay special attention to all printed values and labels.
                    """,
                ],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Bill,
                },
            )

            return Bill.model_validate_json(response.text)

        except Exception as e:
            error_text = str(e)

            if "429" in error_text:
                print(
                    "Gemini rate limit reached. "
                    "Please wait before retrying."
                )
                raise

            if "503" in error_text and attempt == 0:
                print(
                    "Gemini is busy. "
                    "Retrying once in 10 seconds..."
                )
                time.sleep(10)
            else:
                raise