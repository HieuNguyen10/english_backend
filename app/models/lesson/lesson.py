from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.helpers.filter import getByCodeMax


class Lesson(BaseModel):
    __tablename__ = 'w_lesson'

    word_code = Column(String, nullable=False,
                       default=getByCodeMax('w_lesson', 'LS'))
    title = Column(String, nullable=False)

    lesson_word = relationship('LessonWord', back_populates='lesson')
