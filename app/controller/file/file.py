from app.serializers.base import DataResponse
from typing import List, Any, Text
from app.services.base import CRUDBase
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.helpers.security import verify_password, get_password_hash
import logging
from datetime import datetime
from fastapi import Request, APIRouter, Depends, HTTPException, status, UploadFile, File
from app.helpers.paging import Page, PaginationParams, paginate
from app.helpers.filter import getFilter
from app.helpers.login_manager import PermissionRequired
from app.services.file.file import FileService
from sqlalchemy import or_
logger = logging.getLogger()

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Đọc nội dung file từ UploadFile
        contents = await file.read()
        response = False
        response = FileService.upload_file(file=contents, db=db)
        if (response):
            return DataResponse().success(statusCode=status.HTTP_200_OK, data={"message": "Upload success"})
    except Exception as exc:
        # print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.post("/export")
async def export_file(db: Session = Depends(get_db)):
    try:
        return FileService.export_file(db=db)
    except Exception as exc:
        print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])


@router.get("/test")
def test(req: str):
    try:
        response = FileService.get_pronunciation(req)
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])
