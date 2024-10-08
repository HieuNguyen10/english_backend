from pydantic import BaseModel


class WordBase(BaseModel):
    english: str | None = None
    type: str | None = None
    pronunciation: str | None = None
    vietnamese: str | None = None


class WordRequest(BaseModel):
    english: str | None = None
    type: str | None = None
    pronunciation: str | None = None
    vietnamese: str | None = None


class WordResponse(WordBase):
    id: int
    word_code: str

    class Config:
        orm_mode = True


class WordRequestWithLesson(WordRequest):
    word_code_lesson: str | None = 0


class WordVN(BaseModel):
    word_code: str
    vietnamese: str
