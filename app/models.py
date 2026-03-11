#models.py
from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    genre = Column(String, index=True, nullable=True)
    published_date = Column(Date, nullable=True)
    description = Column(String, nullable=True)