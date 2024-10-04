from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.helpers.filter import getByCodeMax


class LessonWord(BaseModel):
    __tablename__ = 'w_lesson_word'

    word_code = Column(String, nullable=False,
                       default=getByCodeMax('w_lesson_word', 'LW'))
    lesson_id = Column(Integer, ForeignKey('w_lesson.id'), nullable=False)
    word_id = Column(Integer, ForeignKey('w_word.id'), nullable=False)

    lesson = relationship('Lesson', back_populates='lesson_word')
    word = relationship('Word', back_populates='lesson_word')
