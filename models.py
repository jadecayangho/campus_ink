from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional


class PrintType(str, Enum):
    """Enum for print types with their prices per page"""
    BLACK_AND_WHITE = "black_and_white"
    COLORED = "colored"
    PHOTO_PAPER = "photo_paper"


class Order(BaseModel):
    """Order model for printing requests"""
    id: Optional[str] = None
    print_type: PrintType
    num_pages: int
    total_cost: float
    created_at: Optional[datetime] = None
    status: str = "pending"  # pending, completed, cancelled
    client_name: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "print_type": "colored",
                "num_pages": 25,
                "total_cost": 125.0,
                "client_name": "John Doe",
                "status": "pending",
                "notes": "Urgent order"
            }
        }


class OrderCreate(BaseModel):
    """Model for creating new orders"""
    print_type: PrintType
    num_pages: int
    client_name: Optional[str] = None
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    """Model for updating orders"""
    print_type: Optional[PrintType] = None
    num_pages: Optional[int] = None
    status: Optional[str] = None
    client_name: Optional[str] = None
    notes: Optional[str] = None
