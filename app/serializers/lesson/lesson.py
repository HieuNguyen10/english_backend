from typing import List
from pydantic import BaseModel
from app.serializers.lesson_word.lesson_word import WordRequest, LessonWordWithWord


class LessonBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class LessonRequest(BaseModel):
    title: str


class LessonResponse(LessonBase):
    word_code: str

    class Config:
        orm_mode = True


class LessonRequestWithWords(LessonRequest):
    word: List[WordRequest] | None = None


class LessonResponseWithWords(LessonBase):
    lesson_word: List[LessonWordWithWord] | None = None

    class Config:
        orm_mode = True
