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
from app.models.word.word import *
from app.serializers.word.word import *
from app.services.word.word import WordService
logger = logging.getLogger()

router = APIRouter()


@router.get("", response_model=Page[WordResponse])
def get(request: Request, text: str | None = None,  page: PaginationParams = Depends(), db: Session = Depends(get_db)):
    try:
        _params = getFilter(request)
        _filter = CRUDBase(Word).filter_query(
            db=db, filter_condition=_params)
        if text is not None:
            ttext = f"%{text}%"
            _filter = _filter.filter(or_(
                Word.english.ilike(ttext),
                Word.vietnamese.ilike(ttext)
            ))
        response = CRUDBase(Word).list(
            db=db, query=_filter, params=page)
        return response
    except Exception as exc:
        print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.get("/{word_code}", response_model=DataResponse[WordResponse])
def get_detail(word_code: str, db: Session = Depends(get_db)):
    try:
        response = CRUDBase(Word).get(db=db, word_code=word_code)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.post("", response_model=DataResponse[WordResponse])
def create(req: WordRequest, db: Session = Depends(get_db)):
    try:
        response = CRUDBase(Word).create(db=db, obj_in=req)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.post("/lesson", response_model=DataResponse[WordResponse])
def creat_with_lesson(req: WordRequestWithLesson, db: Session = Depends(get_db)):
    try:
        response = WordService.creat_word_lessson(req, db)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.put("/{word_code}", response_model=DataResponse[WordResponse])
def update(req: WordRequest, word_code: str, db: Session = Depends(get_db)):
    try:
        data = CRUDBase(Word).get(db=db, word_code=word_code)
        response = CRUDBase(Word).update(
            db=db, obj_in=req, db_obj=data)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.delete("/{word_code}", response_model=DataResponse[WordResponse])
def delete(word_code: str, db: Session = Depends(get_db)):
    try:
        data = CRUDBase(Word).get(db=db, word_code=word_code)
        response = CRUDBase(Word).remove(db=db, db_obj=data)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])
