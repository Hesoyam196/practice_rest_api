import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_item_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name == name).order_by(models.Item.datetime.desc()).first()


def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


def delete_item(db: Session, item_id: int):
    item = db.query(models.Item).filter_by(id=item_id).delete()
    db.commit()
    return


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(name=item.name, price=item.price, datetime=datetime.datetime.now())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    item1 = db.query(models.Item).filter(models.Item.id == item_id).first()
    item1.name = item.name
    item1.price = item.price
    db.add(item1)
    db.commit()
    db.refresh(item1)
    return item1
