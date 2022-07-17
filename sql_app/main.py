from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    return crud.create_item(db=db, item=item)



@app.get("/item/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item



@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.delete('/delete/{item_id}', response_model=dict)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item_id)
    return {"status": "ok"}


@app.put('/update/{item_id}', response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = crud.update_item(db, item_id, item)
    return db_item



