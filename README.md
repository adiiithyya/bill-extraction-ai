# Bill Extraction AI

An AI-powered bill extraction system that converts bill images into structured financial data using multimodal generative AI.

## Overview

Bill Extraction AI analyzes bill and invoice images and extracts important information such as:

- Vendor name
- Invoice number
- Date
- Purchased items
- Quantity
- Unit price
- Item total
- Subtotal
- Tax
- Discount
- Final total

The extracted information is returned as structured JSON and can be validated and evaluated against ground-truth data.

## Features

- Multimodal bill image analysis
- Structured JSON extraction
- Pydantic-based data validation
- Financial consistency validation
- Field-level extraction evaluation
- Multi-bill evaluation
- Streamlit web interface
- JSON export
- Demo mode using previously extracted results
- Retry handling for temporary Gemini service failures

## System Architecture

```text
                Bill Image
                    |
                    v
          +-------------------+
          |   Gemini Flash    |
          | Multimodal Model  |
          +-------------------+
                    |
                    v
          Structured JSON
                    |
                    v
          +-------------------+
          | Pydantic Bill     |
          | Schema Validation |
          +-------------------+
                    |
                    v
          +-------------------+
          | Financial         |
          | Validation        |
          +-------------------+
                    |
                    v
          +-------------------+
          | Streamlit         |
          | Web Interface     |
          +-------------------+
                    |
                    v
              JSON Export
```

## Technologies

- Python
- Google Gemini API
- Generative AI
- Pydantic
- Streamlit
- Git
- GitHub

## Project Structure

```text
bill-extraction/
│
├── bills/
│   └── Sample bill images
│
├── outputs/
│   └── Extracted JSON results
│
├── evaluation/
│   └── ground_truth/
│       └── Ground-truth JSON files
│
├── extractor.py
├── models.py
├── validator.py
├── evaluator.py
├── main.py
├── app.py
├── .env
├── .gitignore
└── README.md
```

## How It Works

### 1. Image Input

A bill image is provided to the system.

Supported formats:

- JPG
- JPEG
- PNG

### 2. Multimodal Extraction

The bill image is sent to the Gemini multimodal model along with an extraction prompt.

The model identifies the relevant information from the image.

### 3. Structured Output

The extracted information is constrained using a Pydantic schema.

The main bill structure contains:

```text
vendor_name
invoice_number
date
items
subtotal
tax
discount
total
```

Each item contains:

```text
name
quantity
unit_price
total
```

### 4. Validation

The system performs financial consistency checks on the extracted information.

For example, it checks whether extracted totals are internally consistent and reports potential mismatches.

### 5. Evaluation

The system compares predicted extraction results against manually prepared ground-truth JSON files.

Evaluation is performed at the field level.

The evaluator checks:

- Vendor name
- Invoice number
- Date
- Subtotal
- Tax
- Discount
- Total
- Item count
- Item names
- Quantities
- Unit prices
- Item totals

### 6. Web Interface

The Streamlit interface allows users to:

1. Upload a bill image
2. Run AI extraction
3. View extracted bill details
4. View item-level information
5. Run financial validation
6. Download the extracted JSON

A Demo Mode is also available for viewing previously generated results without making another API request.

## Evaluation

The current evaluation dataset contains three bills:

| Bill | Field Accuracy |
|------|----------------|
| MYG Invoice | 95.00% |
| Restaurant Invoice | 100.00% |
| Hospital Bill | 100.00% |
| **Average** | **98.33%** |

The MYG invoice contains one remaining date-extraction mismatch, while the other evaluated fields were successfully extracted.

## Installation

Clone the repository:

```bash
git clone https://github.com/adiiithyya/bill-extraction-ai.git
cd bill-extraction-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install google-genai python-dotenv pydantic streamlit
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

## Running the Command-Line Pipeline

```bash
python main.py
```

This processes supported bill images and saves extracted results inside the `outputs/` directory.

## Running the Evaluation

```bash
python evaluator.py
```

The evaluator compares extracted JSON files against the corresponding ground-truth files.

## Running the Streamlit Application

```bash
streamlit run app.py
```

The application can be opened in a browser and used to upload and analyze bill images.

## Security

API credentials are stored in `.env` and excluded from Git using `.gitignore`.

Bill images and generated outputs are also excluded from the public repository.

## Future Improvements

- Improve date extraction for different invoice layouts
- Support additional document formats
- Improve item matching during evaluation
- Add OCR-assisted fallback extraction
- Add confidence scores for extracted fields
- Support batch processing through the web interface
- Add persistent extraction history

## Author

Adithya R Nair