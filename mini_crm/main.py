from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from mini_crm.database import get_db
from mini_crm.schemas import Operator, OperatorCreate, OperatorUpdate, Source, SourceCreate, SourceOperatorWeightCreate, \
    Contact, ContactCreate, Lead
from mini_crm.views import create_operator, get_operators, update_operator, create_source, get_sources, \
    create_source_weight, \
    create_contact, get_contacts, get_leads

app = FastAPI(title="Mini-CRM Lead Distribution")


@app.post("/operators/", response_model=Operator)
def create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):
    return create_operator(db=db, operator=operator)


@app.get("/operators/", response_model=list[Operator])
def read_operators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operators = get_operators(db)
    return operators[skip:skip + limit]


@app.put("/operators/{operator_id}", response_model=Operator)
def update_operator(operator_id: int, operator_update: OperatorUpdate, db: Session = Depends(get_db)):
    operator = update_operator(db, operator_id, operator_update)
    if operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator


@app.post("/sources/", response_model=Source)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    return create_source(db=db, source=source)


@app.get("/sources/", response_model=list[Source])
def read_sources(db: Session = Depends(get_db)):
    return get_sources(db)


@app.post("/source-weights/", response_model=dict)
def create_source_weight(weight: SourceOperatorWeightCreate, db: Session = Depends(get_db)):
    return create_source_weight(db=db, weight=weight)


@app.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        return create_contact(db=db, contact=contact)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/contacts/", response_model=list[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = get_contacts(db)
    return contacts[skip:skip + limit]


@app.get("/leads/", response_model=list[Lead])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = get_leads(db)
    return leads[skip:skip + limit]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
