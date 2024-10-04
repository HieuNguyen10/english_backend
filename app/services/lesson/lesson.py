from fastapi import Depends, File, UploadFile, status
from fastapi.responses import StreamingResponse
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT
from app.serializers.base import DataResponse

from app.services.base import CRUDBase
from sqlalchemy.orm import Session
from app.db.base import get_db

from app.models.word.word import Word
from app.models.lesson.lesson import Lesson
from app.models.lesson_word.lesson_word import LessonWord

from app.serializers.word.word import WordRequestWithLesson, WordVN, WordRequest
from app.serializers.lesson_word.lesson_word import LessonWordRequest
from app.serializers.lesson.lesson import *

from starlette.exceptions import HTTPException
from sqlalchemy import and_


class LessonService(object):
    __instance = None

    @staticmethod
    def creat_with_word(req: LessonRequestWithWords, db: Session = Depends(get_db)):
        try:
            lesson = db.query(Lesson).filter(Lesson.title == req.title).first()
            if (lesson):
                lesson_id = lesson.id
            else:
                lesson = LessonRequest(title=req.title)
                lesson = CRUDBase(Lesson).create(db=db, obj_in=lesson)
                lesson_id = lesson.id
            for word in req.word:
                word = db.query(Word).filter(
                    and_(Word.english == word.english, Word.type == word.type)).first()
                if word is None:
                    word = WordRequest(english=word.english, type=word.type,
                                       pronunciation=word.pronunciation, vietnamese=word.vietnamese)
                    word = CRUDBase(Word).create(db=db, obj_in=word)
                word_id = word.id
                lesson_word = LessonWordRequest(
                    lesson_id=lesson_id, word_id=word_id)
                lesson_word = db.query(LessonWord).filter(
                    and_(LessonWord.lesson_id == lesson_id, LessonWord.word_id == word_id)).first()
                if lesson_word is None:
                    CRUDBase(LessonWord).create(db=db, obj_in=lesson_word)
                return lesson
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
