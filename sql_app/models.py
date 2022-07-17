from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    name = Column(String)
    price = Column(Numeric(10, 2))

    def __repr__(self):
        return f"{self.name} | {self.price}"