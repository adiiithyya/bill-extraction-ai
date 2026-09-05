from pydantic import BaseModel
from typing import Optional, List


class BillItem(BaseModel):
    name: str
    quantity: float
    unit_price: float
    total: float


class Bill(BaseModel):
    vendor_name: str
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    items: List[BillItem]
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    discount: Optional[float] = None
    total: Optional[float] = None