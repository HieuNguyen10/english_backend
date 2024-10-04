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
from app.models.lesson_word.lesson_word import *
from app.serializers.lesson_word.lesson_word import *
logger = logging.getLogger()

router = APIRouter()


@router.get("", response_model=Page[LessonWordResponse])
def get(request: Request, text: str | None = None,  page: PaginationParams = Depends(), db: Session = Depends(get_db)):
    try:
        _params = getFilter(request)
        _filter = CRUDBase(LessonWord).filter_query(
            db=db, filter_condition=_params)
        if text is not None:
            ttext = f"%{text}%"
            _filter = _filter.filter(or_(
                LessonWord.title.ilike(ttext)
            ))
        response = CRUDBase(LessonWord).list(
            db=db, query=_filter, params=page)
        return response
    except Exception as exc:
        print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.get("/{word_code}", response_model=DataResponse[LessonWordWithWord])
def get_detail(word_code: str, db: Session = Depends(get_db)):
    try:
        response = CRUDBase(LessonWord).get(db=db, word_code=word_code)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.post("", response_model=DataResponse[LessonWordResponse])
def create(req: LessonWordRequest, db: Session = Depends(get_db)):
    try:
        response = CRUDBase(LessonWord).create(db=db, obj_in=req)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.put("/{word_code}", response_model=DataResponse[LessonWordResponse])
def update(req: LessonWordRequest, word_code: str, db: Session = Depends(get_db)):
    try:
        data = CRUDBase(LessonWord).get(db=db, word_code=word_code)
        response = CRUDBase(LessonWord).update(
            db=db, obj_in=req, db_obj=data)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.delete("/{word_code}", response_model=DataResponse[LessonWordResponse])
def delete(word_code: str, db: Session = Depends(get_db)):
    try:
        data = CRUDBase(LessonWord).get(db=db, word_code=word_code)
        response = CRUDBase(LessonWord).remove(db=db, db_obj=data)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])
