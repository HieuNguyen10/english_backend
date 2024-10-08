from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.helpers.filter import getByCodeMax


class Word(BaseModel):
    __tablename__ = 'w_word'

    word_code = Column(String, nullable=False,
                       default=getByCodeMax('w_word', 'W'))
    english = Column(String, nullable=False)
    type = Column(String, nullable=True)
    pronunciation = Column(String, nullable=True)
    vietnamese = Column(String, nullable=False)

    lesson_word = relationship('LessonWord', back_populates='word')
