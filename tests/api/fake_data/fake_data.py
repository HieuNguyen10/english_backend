import os
import logging
from datetime import datetime
from fastapi import Request, APIRouter, Depends, HTTPException, status 
from app.helpers.paging import Page, PaginationParams, paginate
from app.models.permission.permission import Permission
from app.serializers.permission.permission import PermissionBase
from app.models.role.role import Role
from app.serializers.role.role import RoleRequestWithPermission
from app.services.role.role import RoleService
from app.serializers.account.account import AccountRequestWithRole
from app.models.account.account import Account 
from app.services.account.account import AccountService
from app.serializers.role_permission.role_permission import RolePermissionBase
from datetime import date
from sqlalchemy import and_
logger = logging.getLogger()
from typing import List
from app.helpers.security import verify_password, get_password_hash
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.services.base import CRUDBase
from app.models.role_permission.role_permission import RolePermission
from app.serializers.base import DataResponse 
from typing import Any
import openpyxl 
import io
router = APIRouter() 
from fastapi.encoders import jsonable_encoder


# POST 
@router.post("/fake_data")
async def fake_data( phone_number: str , db: Session = Depends(get_db)):
    try:
        # fake permission
        file_path = "RolePermission.xlsx"
        if not file_path.endswith(".xlsx"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file format")
        permission_ids = []
        if file_path.endswith(".xlsx"):
            wb = openpyxl.load_workbook(file_path)
            ws = wb["permission_windy_coffee"]
            for cells in ws.iter_rows(min_row=2, values_only=True):
                per = PermissionBase()
                per.name = cells[0]
                per.http_method = cells[1]
                per.pattern = cells[2]
                per.permission_name = cells[3]
                per.description = cells[4]
                per.is_required_access_token = cells[5]
                per.should_check_permission = cells[6]
                
                check_per_exist = db.query(Permission).filter( and_(Permission.is_active==True , Permission.permission_name==per.permission_name , 
                                                              Permission.http_method==per.http_method) ).first()
                if check_per_exist is not None:
                    per_id = check_per_exist.id
                    per_update = CRUDBase(Permission).update(db=db,db_obj=check_per_exist , obj_in=per)
                else:
                    response = CRUDBase(Permission).create(db=db, obj_in=per)
                    per_id = response.id
                permission_ids.append(per_id)
        # fake role
        role_admin = RoleRequestWithPermission(
            name="admin" , 
            permission_id=permission_ids
        )
        check_role = db.query(Role).filter(and_( Role.is_active == True , Role.name=="admin" )).first()
        if check_role is not None: 
            role_id = check_role.id
            for i in permission_ids:
                data_tcp = RolePermissionBase(
                    role_id=role_id,
                    permission_id=i,
                )
                check_role_per = db.query(RolePermission).filter(and_( 
                                                                    RolePermission.is_active == True , 
                                                                    RolePermission.role_id == role_id , 
                                                                    RolePermission.permission_id==i )).first()
                if check_role_per is None: 
                    response = CRUDBase(RolePermission).create(db=db , obj_in=data_tcp) 
        else:
            role = RoleService.create_role_with_permission(data=role_admin , db=db )
            role_id = role.id
        # fake account
        req = AccountRequestWithRole(
            user_name = phone_number, 
            hashed_password = "123456",
            full_name = "Nguyễn Minh Tiến",
            phone_number = phone_number,
            email_address = "minhtien@gmail.com",
            date_of_birth = date(2000, 1, 1),
            gender = 1, 
            address = "Hà Nội",
            avt_url = "image_default", 
            role_id = role_id
        )
        account_exist = AccountService.check_account(req , db) 
        if account_exist:
            return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Phone number already exist"]) 
        #req.user_name = req.phone_number 
        match = AccountService.check_phone_number(req.phone_number, db)
        if not match:
            return DataResponse().errors(
                statusCode=status.HTTP_409_CONFLICT,
                error=["Invalid phone number"],
            )
        response = CRUDBase(Account).create(db=db, obj_in=req)      
        if response is None:
            return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Creating account failed"]) 
        return DataResponse().success(statusCode=status.HTTP_200_OK, data=response)
    except Exception as exc:
        print(exc)
        return DataResponse().errors(statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY, error=["Something went wrong"])
    

