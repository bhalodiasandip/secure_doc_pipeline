# run_pipeline.py
import json
from pydantic.json import pydantic_encoder
from pipeline.pipeline import ProcessingPipeline


"""
This script demonstrates two sample runs:
1) Success case: Valid JSON string that matches the Pydantic model constraints.
2) Failure case: Valid JSON string but fails Pydantic validation (total_amount <= 0).
"""

pipeline = ProcessingPipeline()

# 1) Success case - using data similar to the uploaded PDF `Logistics_Invoice_IN-horus-987103.pdf`
success_input = json.dumps({
    "document_type": "INVOICE",
    "supplier_name": "GLOBAL LOGISTICS SOLUTIONS LTD.",
    "invoice_date": "2025-11-28",
    "total_amount": 7720.00,
    "line_items": [
        {"description": "Air Freight, EU-US", "quantity": 4, "unit_price": 1250.00},
        {"description": "Ocean Cargo, APAC", "quantity": 2, "unit_price": 800.00},
        {"description": "Standard VAT (20%)", "quantity": 1, "unit_price": 1320.00},
        {"description": "Loyalty Discount", "quantity": 1, "unit_price": -200.00}
    ]
})

print("\n--- Running SUCCESS case ---")
success_result = pipeline.process_document(success_input, "Logistics_Invoice_IN-horus-987103.pdf")
print("Result:", json.dumps(success_result, indent=2, default=pydantic_encoder))

# 2) Failure case - valid JSON but fails validation: total_amount is 0 (invalid, must be > 0)
failure_input = json.dumps({
    "document_type": "INVOICE",
    "supplier_name": "GLOBAL LOGISTICS SOLUTIONS LTD.",
    "invoice_date": "2025-11-28",
    "total_amount": 0.0,  # invalid: must be > 0
    "line_items": [
        {"description": "Air Freight, EU-US", "quantity": 4, "unit_price": 1250.00}
    ]
})

print("\n--- Running FAILURE case (validation error) ---")
failure_result = pipeline.process_document(failure_input, "invalid_invoice.json")
print("Result:", json.dumps(failure_result, indent=2))
