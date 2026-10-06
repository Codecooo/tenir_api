from ninja import Schema
from typing import Optional

class MountainSchema(Schema):
    """Schema untuk Mountain model - Response format"""
    id: int
    name: str
    location: str
    description: str
    height: float
    difficulty_level: str
    region: str
    indonesian_weekday_price: float
    indonesian_weekend_price: float
    international_weekday_price: float
    international_weekend_price: float
    alert_level: str

class MountainCreateSchema(Schema):
    """Schema untuk create mountain - Request format"""
    name: str
    location: str
    description: str
    height: float
    difficulty_level: str
    region: str
    indonesian_weekday_price: float
    indonesian_weekend_price: float
    international_weekday_price: float
    international_weekend_price: float
    alert_level: str

class MountainUpdateSchema(Schema):
    """Schema untuk update mountain"""
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    height: Optional[float] = None
    difficulty_level: Optional[str] = None
    region: Optional[str] = None
    indonesian_weekday_price: Optional[float] = None
    indonesian_weekend_price: Optional[float] = None
    international_weekday_price: Optional[float] = None
    international_weekend_price: Optional[float] = None
    alert_level: Optional[str] = None