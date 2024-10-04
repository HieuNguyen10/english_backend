from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.helpers.paging import PaginationParams, paginate
from app.models.base import BaseModel
from sqlalchemy import func, func, and_
from app.helpers.security import verify_password, get_password_hash
ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    _instances = {}

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model oc_class
        * `schema`: A Pydantic model (schema) oc_class
        """
        self.model = model

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                CRUDBase, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]

    def getCode(self, db: Session, sku: str = 'OC'):
        result = db.query(func.max(self.model.id)).first()
        if (result[0] is not None):
            return sku + '0000' + str(result[0] + 1)
        return sku + '00001'

    def getById(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id, self.model.is_active == True).first()

    def get(self, db: Session, word_code: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.word_code == word_code, self.model.is_active == True).first()

    def list(self, db: Session, *, query: Query, params: Optional[PaginationParams]) -> Optional[Any]:
        results = paginate(model=self.model, query=query, params=params)

        return results

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        if "hashed_password" in obj_in_data:
            obj_in_data["hashed_password"] = get_password_hash(
                obj_in_data["hashed_password"])
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def creates(self, db: Session, *, objs_in: CreateSchemaType) -> ModelType:
        objects = []
        for obj_in in objs_in:
            db_item = self.model(**obj_in)
            objects.append(db_item)
        db.bulk_insert_mappings(objects)
        db.commit()
        db.refresh(objects)
        return objects

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(self, db: Session, *, word_code: int) -> ModelType:
        obj = db.query(self.model).filter(self.model.word_code ==
                                          word_code, self.model.is_active == True).first()

        db.delete(obj)
        db.commit()

        return obj

    def destroy(self, db: Session, *, db_obj: ModelType) -> ModelType:
        db_obj.is_active = False

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def filter_query(self, db: Session, filter_condition) -> Any:
        '''
        Return filtered queryset based on condition.
        :param query: takes query
        :param filter_condition: Its a list, ie: [(key,operator,value)]
        operator list:
            eq for ==
            lt for <
            ge for >=
            in for in_
            like for like
            value could be list or a string
        :return: queryset
        '''
        query = db.query(self.model).filter(self.model.is_active == True)
        for raw in filter_condition:
            try:
                key, op, value = raw
            except ValueError:
                raise Exception('Invalid filter: %s' % raw)
            column = getattr(self.model, key, None)
            if not column:
                raise Exception('Invalid filter column: %s' % key)
            if op == 'in':
                if isinstance(value, list):
                    filt = column.in_(value)
                else:
                    filt = column.in_(value.split(','))
            elif op == 'like':
                filt = column.like(f"%{value}%")
            elif op == 'ilike':
                filt = column.ilike(f"%{value}%")
            else:
                try:
                    attr = list(filter(
                        lambda e: hasattr(column, e % op),
                        ['%s', '%s_', '__%s__']
                    ))[0] % op
                except IndexError:
                    raise Exception('Invalid filter operator: %s' % op)
                if value == 'null':
                    value = None
                filt = getattr(column, attr)(value)
            query = query.filter(filt)
        return query
