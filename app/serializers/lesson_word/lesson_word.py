from pydantic import BaseModel
from app.serializers.word.word import WordRequest, WordResponse


class LessonWordBase(BaseModel):
    lesson_id: int
    word_id: int


class LessonWordRequest(BaseModel):
    lesson_id: int
    word_id: int


class LessonWordResponse(LessonWordBase):
    word_code: str

    class Config:
        orm_mode = True


class LessonWordWithWord(LessonWordBase):
    word: WordResponse | None = None

    class Config:
        orm_mode = True
