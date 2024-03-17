__all__ = ("User",)

from typing import Any

from sqlalchemy import Column, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base


Base: Any = declarative_base()


class User(Base):
    __tablename__ = "users"

    telegram_id: Column[int] = Column(Integer, primary_key=True)
    age: Column[int] = Column(SmallInteger, nullable=False)
    bio: Column[str] = Column(String(100), nullable=True)
    country: Column[str] = Column(String(100), nullable=False)
    city: Column[str] = Column(String(100), nullable=False)
