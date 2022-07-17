import datetime
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sql_app.database import SessionLocal, engine
from sql_app import models

SQLALCHEMY_DATABASE_URL = "sqlite:///database.sqlite"
PRODUCT_URL = 'https://mebel-ekb.com/category/modulnye-spalni/modulnaya-spalnya-linate/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
}

page = requests.get(url=PRODUCT_URL, headers=headers)
soup = BeautifulSoup(page.content, 'lxml')
name = soup.find('h1').get_text()
price = int(soup.find('i', class_='price').get_text().replace('руб.', '').replace(' ', ''))

Base = declarative_base()


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    name = Column(String)
    price = Column(Numeric(10, 2))

    def __repr__(self):
        return f"{self.name} | {self.price}"


models.Base.metadata.create_all(engine)
#session = Session(bind=engine)
session = SessionLocal()

is_exist = session.query(Item).filter(Item.name == name).first()
if not is_exist:
    session.add(
        Item(name=name, price=price, datetime=datetime.datetime.now())
    )
    session.commit()

items = session.query(Item).all()
for item in items:
    print(item)