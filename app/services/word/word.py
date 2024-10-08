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
from app.serializers.lesson.lesson import LessonRequest

from starlette.exceptions import HTTPException
from sqlalchemy import and_
import re
import http.client
import json


class WordService(object):
    __instance = None

    @staticmethod
    def creat_word_lessson(req: WordRequestWithLesson, db: Session = Depends(get_db)):
        try:
            lesson = db.query(Lesson).filter(
                Lesson.title == req.word_code_lesson).first()
            if (not lesson):
                lesson = LessonRequest(title=req.word_code_lesson)
                lesson = CRUDBase(Lesson).create(db=db, obj_in=lesson)
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
            if (req.pronunciation == "" or req.pronunciation is None):
                req.pronunciation = WordService.get_pronunciation(req.english)
                if req.pronunciation is None:
                    req.pronunciation = ""
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

    @staticmethod
    def delete_word(word_code: str, db: Session = Depends(get_db)):
        try:
            word = CRUDBase(Word).get(db=db, word_code=word_code)
            if (not word):
                raise HTTPException(status_code=400, detail="Word not found")
            lesson_word = db.query(LessonWord).filter(
                LessonWord.word_id == word.id).all()
            for lw in lesson_word:
                CRUDBase(LessonWord).remove(db=db, word_code=lw.word_code)
            word = CRUDBase(Word).remove(db=db, word_code=word_code)
            return word
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def get_pronunciation(word: str):
        try:
            if len(word.split()) > 1:
                print("Word contains two or more words. Returning None.")
                return ""  # Trả về None nếu có hai từ trở lên
            conn = http.client.HTTPSConnection("wordsapiv1.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': "221957c4b0mshd706e530a711a31p1dc28djsn963cbb20f6cf",
                'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
            }
            conn.request(
                "GET", f"/words/{word}/pronunciation", headers=headers)
            res = conn.getresponse()
            data = res.read()
            pronunciation_data = json.loads(data)
            pronunciation = pronunciation_data.get("pronunciation")
            if isinstance(pronunciation, dict) and 'all' in pronunciation:
                # Lấy giá trị từ thuộc tính 'all'
                pronunciation_value = pronunciation['all']
            else:
                pronunciation_value = pronunciation  # Lấy trực tiếp giá trị phát âm
            print(pronunciation_value)
            return pronunciation_value
        except Exception as exc:
            return None
