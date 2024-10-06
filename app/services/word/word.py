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

from starlette.exceptions import HTTPException
from sqlalchemy import and_
import re


class WordService(object):
    __instance = None

    @staticmethod
    def creat_word_lessson(req: WordRequestWithLesson, db: Session = Depends(get_db)):
        try:
            lesson = CRUDBase(Lesson).get(
                db=db, word_code=req.word_code_lesson)
            if (not lesson):
                raise HTTPException(status_code=400, detail="Lesson not found")
            lesson_id = lesson.id
            word = db.query(Word).filter(
                and_(Word.english == req.english, Word.type == req.type)).first()
            if (word):
                word_id = word.id
                lesson_word = db.query(LessonWord).filter(
                    and_(LessonWord.lesson_id == lesson_id, LessonWord.word_id == word_id)).first()
                if (lesson_word):
                    return word
                lesson_word = LessonWordRequest(
                    lesson_id=lesson_id, word_id=word_id)
                try:
                    lesson_word = CRUDBase(LessonWord).create(
                        db=db, obj_in=lesson_word)
                except Exception as e:
                    print(e)
                return word
            word = WordRequest(english=req.english, type=req.type,
                               pronunciation=req.pronunciation, vietnamese=req.vietnamese)
            word = CRUDBase(Word).create(db=db, obj_in=word)
            word_id = word.id
            lesson_word = LessonWordRequest(
                lesson_id=lesson_id, word_id=word_id)
            CRUDBase(LessonWord).create(db=db, obj_in=lesson_word)
            return word
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def update_vn(req: WordVN, db: Session = Depends(get_db)):
        try:
            word = CRUDBase(Word).get(db=db, word_code=req.word_code)
            if (not word):
                raise HTTPException(status_code=400, detail="Word not found")
            word = CRUDBase(Word).update(db=db, db_obj=word, obj_in=req)
            return word
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
