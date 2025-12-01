from sqlalchemy.orm import Session

from . import models, schemas
from .services import distribute_contact


def create_operator(db: Session, operator: schemas.OperatorCreate):
    """Функция создания оператора в базе."""
    db_operator = models.Operator(**operator.model_dump())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


def get_operators(db: Session):
    """Функция для получения всех операторов из базы данных."""
    return db.query(models.Operator).all()


def get_operator(db: Session, operator_id: int):
    """Функция для получения конкретного оператора по ID из базы данных."""
    return db.query(models.Operator).filter(models.Operator.id == operator_id).first()


def update_operator(db: Session, operator_id: int, operator_update: schemas.OperatorUpdate):
    """Функция обновления данных оператора в базе данных."""
    operator = get_operator(db, operator_id)
    if operator:
        update_data = operator_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(operator, field, value)
        db.commit()
        db.refresh(operator)
    return operator


def create_source(db: Session, source: schemas.SourceCreate):
    """Функция для создания источника в базе данных."""
    db_source = models.Source(**source.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_sources(db: Session):
    """Функция для получения всех источников из базы данных."""
    return db.query(models.Source).all()


def create_source_weight(db: Session, weight: schemas.SourceOperatorWeightCreate):
    """Функция для создания веса источника на оператора в базе данных."""
    db_weight = models.SourceOperatorWeight(**weight.model_dump())
    db.add(db_weight)
    db.commit()
    db.refresh(db_weight)
    return db_weight


def get_or_create_lead(db: Session, external_id: str) -> models.Lead:
    """Функция для создания или получения лида из базы данных."""
    lead = db.query(models.Lead).filter(models.Lead.external_id == external_id).first()
    if not lead:
        lead = models.Lead(external_id=external_id)
        db.add(lead)
        db.commit()
        db.refresh(lead)
    return lead


def create_contact(db: Session, contact: schemas.ContactCreate) -> models.Contact:
    """Функция для создания контакта в базе данных."""

    # находим/создаем лида
    lead = get_or_create_lead(db, contact.external_id)

    # находим источник
    source = db.query(models.Source).filter(
        models.Source.name == contact.source_name
    ).first()
    if not source:
        raise ValueError(f"Источник {contact.source_name} не найден")

    # распределяем оператора
    operator_id = distribute_contact(db, source.id)

    # создаем обращение
    db_contact = models.Contact(
        lead_id=lead.id,
        source_id=source.id,
        operator_id=operator_id,
        message=contact.message
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session):
    """Функция для получения всех контактов из базы данных."""
    return db.query(models.Contact).all()


def get_leads(db: Session):
    """Функция для получения всех лидов из базы данных."""
    return db.query(models.Lead).all()
