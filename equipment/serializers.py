from ninja import Schema
from typing import Optional

class EquipmentSchema(Schema):
    """Schema untuk Equipment - Response format"""
    id: int
    name: str
    description: str
    category: str
    daily_rental_price: float
    total_quantity: int
    available_quantity: int
    condition: str
    weight: Optional[float] = None
    size: Optional[str] = None
    color: Optional[str] = None
    image: Optional[str] = None
    created_at: str
    updated_at: str


class EquipmentCreateSchema(Schema):
    """Schema untuk create equipment - Request format"""
    name: str
    description: str
    category: str
    daily_rental_price: float
    total_quantity: int = 1
    available_quantity: int = 1
    condition: str = 'GOOD'
    weight: Optional[float] = None
    size: Optional[str] = None
    color: Optional[str] = None


class EquipmentUpdateSchema(Schema):
    """Schema untuk update equipment"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    daily_rental_price: Optional[float] = None
    total_quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    condition: Optional[str] = None
    weight: Optional[float] = None
    size: Optional[str] = None
    color: Optional[str] = None