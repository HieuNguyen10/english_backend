from app.serializers.base import DataResponse
from typing import List, Any
from app.services.base import CRUDBase
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.helpers.security import verify_password, get_password_hash
import logging
from datetime import datetime
from fastapi import Request, APIRouter, Depends, HTTPException, status
from app.helpers.paging import Page, PaginationParams, paginate
from app.helpers.filter import getFilter
from app.helpers.login_manager import PermissionRequired
from sqlalchemy import or_
from app.models.lesson.lesson import *
from app.models.lesson_word.lesson_word import *
from app.serializers.lesson.lesson import *
from app.services.lesson.lesson import LessonService
logger = logging.getLogger()

router = APIRouter()


@router.get("", response_model=Page[LessonResponse])
def get(request: Request, text: str | None = None,  page: PaginationParams = Depends(), db: Session = Depends(get_db)):
    try:
        _params = getFilter(request)
        _filter = CRUDBase(Lesson).filter_query(
            db=db, filter_condition=_params)
        if text is not None:
            ttext = f"%{text}%"
            _filter = _filter.filter(or_(
                Lesson.title.ilike(ttext)
            ))
        response = CRUDBase(Lesson).list(
            db=db, query=_filter, params=page)
        return response
    except Exception as exc:
        print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.get("/{word_code}", response_model=DataResponse[LessonResponseWithWords])
def get_detail(word_code: str, db: Session = Depends(get_db)):
    try:
        response = CRUDBase(Lesson).get(db=db, word_code=word_code)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.post("", response_model=DataResponse[LessonResponse])
def create(req: LessonRequest, db: Session = Depends(get_db)):
    try:
        response = CRUDBase(Lesson).create(db=db, obj_in=req)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.post("/word", response_model=DataResponse[LessonResponseWithWords])
def creat_with_word(req: LessonRequestWithWords, db: Session = Depends(get_db)):
    try:
        response = LessonService.creat_with_word(req, db)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.put("/{word_code}", response_model=DataResponse[LessonResponse])
def update(req: LessonRequest, word_code: str, db: Session = Depends(get_db)):
    try:
        data = CRUDBase(Lesson).get(db=db, word_code=word_code)
        response = CRUDBase(Lesson).update(
            db=db, obj_in=req, db_obj=data)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.delete("/{word_code}", response_model=DataResponse[LessonResponse])
def delete(word_code: str, db: Session = Depends(get_db)):
    try:
        data = CRUDBase(Lesson).get(db=db, word_code=word_code)
        if (not data):
            return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Not found"])
        lesson_word = db.query(LessonWord).filter(
            LessonWord.lesson_id == data.id).all()
        for lw in lesson_word:
            CRUDBase(LessonWord).remove(db=db, word_code=lw.word_code)
        response = CRUDBase(Lesson).remove(db=db, word_code=data.word_code)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.post("/full", response_model=DataResponse[List[LessonResponse]])
def get_full_lesson(db: Session = Depends(get_db)):
    try:
        lessons = db.query(Lesson).all()  # Lấy tất cả dữ liệu từ bảng Lesson
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=lessons)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])
