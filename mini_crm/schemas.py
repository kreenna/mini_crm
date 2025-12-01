from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class OperatorBase(BaseModel):
    """Базовая модель оператора Pydantic."""
    name: str
    max_active_leads: int = 10
    is_active: bool = True


class OperatorCreate(OperatorBase):
    """Функциональность создания оператора Pydantic."""
    pass


class OperatorUpdate(BaseModel):
    """Функциональность обновления оператора Pydantic."""
    name: Optional[str] = None
    max_active_leads: Optional[int] = None
    is_active: Optional[bool] = None


class Operator(OperatorBase):
    """Модель оператора с конфигурацией Pydantic."""
    id: int
    current_active_leads: int

    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    """Базовая модель источника Pydantic."""
    name: str


class SourceCreate(SourceBase):
    """Функциональность создания источника Pydantic."""
    pass


class Source(SourceBase):
    """Модель источника с конфигурацией Pydantic."""
    id: int

    class Config:
        from_attributes = True


class SourceOperatorWeightBase(BaseModel):
    """Базовая модель веса источника на оператора Pydantic."""
    source_id: int
    operator_id: int
    weight: float = 1.0


class SourceOperatorWeightCreate(SourceOperatorWeightBase):
    """Функциональность создания веса источника на оператора Pydantic."""
    pass


class LeadBase(BaseModel):
    """Базовая модель лида Pydantic."""
    external_id: str


class LeadCreate(LeadBase):
    """Функциональность создания лида Pydantic."""
    pass


class Lead(LeadBase):
    """Модель лида с конфигурацией Pydantic."""
    id: int
    created_at: datetime
    contacts: List['Contact'] = []

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    """Базовая модель контакта Pydantic."""
    external_id: str  # для лида
    source_name: str
    message: Optional[str] = None


class Contact(ContactCreate):
    """Функциональность создания контакта Pydantic."""
    id: int
    lead_id: int
    source_id: int
    operator_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
