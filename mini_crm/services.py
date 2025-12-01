import random
from typing import Optional

from sqlalchemy.orm import Session

from . import models


def distribute_contact(db: Session, source_id: int) -> Optional[int]:
    """Функция для распределения обращения по весам операторов."""

    # получаем доступных операторов для источника
    weights = db.query(models.SourceOperatorWeight).filter(
        models.SourceOperatorWeight.source_id == source_id
    ).join(
        models.Operator, models.SourceOperatorWeight.operator_id == models.Operator.id
    ).filter(
        models.Operator.is_active == True,
        models.Operator.current_active_leads < models.Operator.max_active_leads
    ).all()

    if not weights:
        return None  # нет доступных операторов

    # вычисляем вероятности
    total_weight = sum(w.weight for w in weights)
    probabilities = [(w.weight / total_weight, w.operator_id) for w in weights]

    # случайный выбор по весам
    operator_id = random.choices(
        [probability[1] for probability in probabilities],
        weights=[probability[0] for probability in probabilities],
        k=1
    )[0]

    # обновляем нагрузку оператора
    operator = db.query(models.Operator).filter(
        models.Operator.id == operator_id
    ).first()
    operator.current_active_leads += 1
    db.commit()

    return operator_id
