# Mini-CRM Lead Distribution System
Мини-CRM для распределения лидов между операторами по источникам с учетом весов и лимитов нагрузки.

---

## Быстрый запуск (2 минуты)

1. Клонировать/распаковать проект

```
git clone https://github.com/kreenna/mini_crm && cd mini-crm
```

2. Установить зависимости

```
pip install -r requirements.txt
```

3. Применить миграции

```
alembic upgrade head
```

4. Запустить сервер

```
uvicorn app.main:app --reload --port 8000
```

API доступно: http://127.0.0.1:8000/docs

---

## Полная последовательность команд

```
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

---

### Ключевые сущности:

- Operator: активность, лимит активных лидов, веса по источникам

- Lead: external_id (уникальный: телефон/email)

- Source: бот/канал с настройками операторов+весов

- Contact: обращение (лид+источник+оператор)

- Нагрузка оператора: current_active_leads < max_active_leads

---

### Бизнес-логика распределения

- Поиск/создание лида по external_id

- Доступные операторы: is_active=True + current_active_leads < max_active_leads

- Выбор по весам: random.choices(weights) среди доступных

- Нет операторов → обращение без оператора (operator_id=NULL)

---

### API Эндпоинты
- ```POST	/operators/``` Создать оператора
- ```GET	/operators/``` Список операторов
- ```PUT	/operators/{id}``` Обновить лимит/активность
- ```POST	/sources/``` Создать источник (бот)
- ```POST	/source-weights/``` Настроить веса операторов
- ```POST	/contacts/``` Создать обращение (главный!)
- ```GET	/contacts/``` Список обращений
- ```GET	/leads/``` Список лидов

---

### Миграции Alembic

```
# статус
alembic current

# новая миграция (при изменении моделей)
alembic revision --autogenerate -m "add_field"

# применить
alembic upgrade head

# откат
alembic downgrade -1
```

---

### Примеры запросов (curl)

```
# создать операторов
curl -X POST "http://127.0.0.1:8001/operators/" -H "Content-Type: application/json" -d '{"name": "Иван", "max_active_leads": 5}'

curl -X POST "http://127.0.0.1:8001/operators/" -H "Content-Type: application/json" -d '{"name": "Мария", "max_active_leads": 10}'

# создать источник
curl -X POST "http://127.0.0.1:8001/sources/" -H "Content-Type: application/json" -d '{"name": "telegram_bot"}'

# настроить веса (Иван:30%, Мария:70%)
curl -X POST "http://127.0.0.1:8001/source-weights/" -H "Content-Type: application/json" -d '{"source_id":1,"operator_id":1,"weight":3}'
curl -X POST "http://127.0.0.1:8001/source-weights/" -H "Content-Type: application/json" -d '{"source_id":1,"operator_id":2,"weight":7}'

# создать обращение (автоматическое распределение)
curl -X POST "http://127.0.0.1:8001/contacts/" -H "Content-Type: application/json" -d '{"external_id":"+79123456789","source_name":"telegram_bot","message":"Нужна консультация"}'
```

---