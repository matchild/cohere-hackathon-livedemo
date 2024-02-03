import datetime

from sqlalchemy.orm import Session

from app.db.models import DataframeORM, ValueORM, VariableORM
from app.db.schemas import Dataframe, Value, Variable


# DataframeORM
def get_dataframe_by_id(db: Session, id: int) -> DataframeORM | None:
    return db.query(DataframeORM).filter_by(id=id).first()


def register_dataframe(db: Session, object_in: Dataframe) -> DataframeORM:
    object_dict = object_in.dict()
    object_dict["registered_at"] = datetime.datetime.utcnow()

    db_object = DataframeORM(**object_dict)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


# VariableORM
def get_variable_by_id(db: Session, id: int) -> VariableORM | None:
    return db.query(VariableORM).filter_by(id=id).first()


def register_variable(db: Session, object_in: Variable) -> VariableORM:
    object_dict = object_in.dict()
    object_dict["registered_at"] = datetime.datetime.utcnow()

    db_object = VariableORM(**object_dict)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


# ValueORM
def get_value_by_id(db: Session, id: int) -> ValueORM | None:
    return db.query(ValueORM).filter_by(id=id).first()


def register_value(db: Session, object_in: Value) -> ValueORM:
    object_dict = object_in.dict()
    object_dict["registered_at"] = datetime.datetime.utcnow()

    db_object = ValueORM(**object_dict)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object
