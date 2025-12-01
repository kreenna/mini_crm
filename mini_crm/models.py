from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class Operator(Base):
    """Модель оператора."""
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    max_active_leads = Column(Integer, default=10)
    current_active_leads = Column(Integer, default=0)

    source_weights = relationship("SourceOperatorWeight", back_populates="operator")
    contacts = relationship("Contact", back_populates="operator")


class Lead(Base):
    """Модель лида."""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)  # телефон/email
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    contacts = relationship("Contact", back_populates="lead")


class Source(Base):
    """Модель источника."""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)  # bot1, bot2

    weights = relationship("SourceOperatorWeight", back_populates="source")
    contacts = relationship("Contact", back_populates="source")


class SourceOperatorWeight(Base):
    """Модель веса источника на оператора."""
    __tablename__ = "source_operator_weights"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"))
    weight = Column(Float, default=1.0)

    source = relationship("Source", back_populates="weights")
    operator = relationship("Operator", back_populates="source_weights")


class Contact(Base):
    """Модель контакта."""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String, nullable=True)

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")
