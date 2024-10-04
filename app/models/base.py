from datetime import datetime
from pydantic import validator

from sqlalchemy import Column, Integer, DateTime, Boolean, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr

DeclarativeBase = declarative_base()


@as_declarative()
class BaseCustom:
    __abstract__ = True
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(BaseCustom):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    word_code = Column(String, index=True, nullable=True, default=None)
    is_active = Column('is_active', Boolean, index=True, default=True)
    created_at = Column('created_at', DateTime(
        timezone=True), index=True, default=func.now())
    updated_at = Column('updated_at', DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
