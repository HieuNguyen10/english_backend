from fastapi import HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
# from app.models.permission.permission import Permission
from typing import List
from app.helpers.security import reusable_oauth2

# from app.models.role.role import Role
# from app.models.permission.permission import Permission
# from app.models.role_permission.role_permission import RolePermission
from sqlalchemy import and_
import jwt
from app.helpers.config import settings
from app.serializers.base import DataResponse
from app.helpers.security import validate_token


def get_current_role_user(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get user_id => return User info from DB query
    """
    try:
        payload = jwt.decode(
            http_authorization_credentials.credentials, settings.SECRET_KEY,
            algorithms=[settings.SECURITY_ALGORITHM]
        )
        role_id = payload["role_id"]

    except (Exception):
        raise HTTPException(status_code=404, detail="User not found")
    role = db.session.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="User not found")
    return role


def login_required(http_authorization_credentials=Depends(reusable_oauth2)):
    role_user = get_current_role_user(http_authorization_credentials)
    return role_user


class PermissionRequired:
    def __init__(self, permission):
        self.role = None
        self.permissions = permission

    # def __call__(self, user: Role = Depends(validate_token)):
    def __call__(self):

        try:
            # # tạm check true để đợi permission_name có đủ
            # self.user = user
            # auth_info = jsonable_encoder(user)
            # list_permission_name = []
            # role = db.session.query(Role).filter(and_(Role.is_active == True,
            #                                           Role.id == auth_info['role_id']
            #                                           )).first()
            # if role is None:
            #     raise HTTPException(
            #         status_code=400, detail=f'User can not access this api')
            # role_permission = db.session.query(RolePermission).filter(and_(RolePermission.is_active == True,
            #                                                                RolePermission.role_id == auth_info['role_id'])).all()
            # for i in role_permission:
            #     permission = db.session.query(Permission).filter(
            #         and_(Permission.is_active == True, Permission.id == i.permission_id)).first()
            #     if permission.is_required_access_token == 0 or permission.should_check_permission == 0:
            #         continue
            #     permission_name = permission.permission_name
            #     list_permission_name.append(permission_name)
            # if self.permissions not in list_permission_name and self.permissions or len(list_permission_name) <= 0:
            #     raise HTTPException(
            #         status_code=401, detail=f'User can not access this api')
            return True
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=401, detail=f'User can not access this api')


# def login_required(http_authorization_credentials=Depends(UserService().reusable_oauth2)):
#     return UserService().get_current_user(http_authorization_credentials)

# # Check User và Role
# class PermissionRequired:
#     def __init__(self, *args):
#         self.user = None
#         self.permissions = args

#     def __call__(self, user: User = Depends(login_required)):
#         self.user = user
#         if self.user.role not in self.permissions and self.permissions:
#             raise HTTPException(status_code=400,
#                                 detail=f'User {self.user.email} can not access this api')


#                                                                                                                   Anh Thọ
# def login_required(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#     user_id = Authorize.get_jwt_subject()
#     current_user = db.session.query(Account).filter_by(id=user_id).first()
#     return current_user


# class PermissionRequired:
#     def __init__(self, *args):
#         self.account = None
#         self.permissions = args

    # def __call__(self, account: Account = Depends(login_required)):
    #     self.account = account
    #     if self.account.role not in self.permissions and self.permissions:
    #         raise HTTPException(status_code=400,
    #                             detail=f'User {self.user.email} can not access this api')
