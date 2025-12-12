# models/models.py
from __future__ import annotations
from typing import List, Optional, Annotated
from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field, StringConstraints


class LineItem(BaseModel):
    description: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    quantity: Annotated[int, Field(ge=1)]
    unit_price: float


class StandardDocumentData(BaseModel):
    audit_id: Optional[UUID]
    document_type: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    supplier_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    invoice_date: date
    total_amount: Annotated[float, Field(gt=0)]
    line_items: List[LineItem]

    model_config = {
        "str_strip_whitespace": True
    }
