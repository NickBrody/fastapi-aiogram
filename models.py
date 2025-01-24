from sqlalchemy import Column, String, Integer, Float
from database import Base

class Product(Base):
    __tablename__ = 'products'

    name = Column(String, primary_key=True)
    articul = Column(Integer, nullable=True)
    price = Column(Float)
    rating = Column(Float, nullable=True)
    total = Column(Integer)

