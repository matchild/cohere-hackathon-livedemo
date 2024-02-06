import datetime
import logging

from sqlalchemy.orm import Session

from app.db.models import DataframeORM, UnstructuredORM, ValueORM, VariableORM
from app.db.schemas import Dataframe, DataframeFull, Unstructured, Value, Variable
from app.db.vectorstore import orm_to_vectorstore, unstructured_orm_to_vectorstore


# DataframeORM
def get_dataframe_by_id(db: Session, id: int) -> DataframeORM | None:
    return db.query(DataframeORM).filter_by(id=id).first()


def register_dataframe(db: Session, object_in: Dataframe) -> DataframeORM:
    object_dict = object_in.model_dump()
    object_dict["registered_at"] = datetime.datetime.utcnow()

    db_object = DataframeORM(**object_dict)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)

    logging.info(f"Adding dataframe with id={db_object.id} to vectorstore...")
    vectorstore_id = orm_to_vectorstore(db_object)
    db_object.vectorstore_id = vectorstore_id
    db.commit()

    return db_object


# VariableORM
def get_variable_by_id(db: Session, id: int) -> VariableORM | None:
    return db.query(VariableORM).filter_by(id=id).first()


def register_variable(db: Session, object_in: Variable) -> VariableORM:
    object_dict = object_in.model_dump()
    object_dict["registered_at"] = datetime.datetime.utcnow()

    db_object = VariableORM(**object_dict)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)

    logging.info(f"Adding variable with id={db_object.id} to vectorstore...")
    vectorstore_id = orm_to_vectorstore(db_object)
    db_object.vectorstore_id = vectorstore_id
    db.commit()

    return db_object


# ValueORM
def get_value_by_id(db: Session, id: int) -> ValueORM | None:
    return db.query(ValueORM).filter_by(id=id).first()


def register_value(db: Session, object_in: Value) -> ValueORM:
    object_dict = object_in.model_dump()
    object_dict["registered_at"] = datetime.datetime.utcnow()

    db_object = ValueORM(**object_dict)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)

    logging.info(f"Adding value with id={db_object.id} to vectorstore...")
    vectorstore_id = orm_to_vectorstore(db_object)
    db_object.vectorstore_id = vectorstore_id
    db.commit()

    return db_object


# Full
def register_full_dataframe(
    db: Session,
    dataframe_in: DataframeFull,
) -> None:

    db_dataframe = register_dataframe(
        db, Dataframe(name=dataframe_in.name, description=dataframe_in.description)
    )

    for variable_in in dataframe_in.variables:
        db_variable = register_variable(
            db,
            Variable(
                dataframe_id=db_dataframe.id,
                name=variable_in.name,
                description=variable_in.description,
                is_categorical=variable_in.is_categorical,
            ),
        )

        if not variable_in.is_categorical and len(variable_in.values) > 0:
            raise Exception(
                f"Variable {variable_in.name} is not categorical but has values provided"
            )

        for value_in in variable_in.values:
            db_value = register_value(
                db,
                Value(
                    variable_id=db_variable.id,
                    name=value_in.name,
                    description=value_in.description,
                ),
            )


# UnstructuredORM
def get_unstructured_by_id(db: Session, id: int) -> UnstructuredORM | None:
    return db.query(UnstructuredORM).filter_by(id=id).first()


def register_unstructured(db: Session, object_in: Unstructured) -> UnstructuredORM:
    object_dict = object_in.model_dump()
    object_dict["registered_at"] = datetime.datetime.utcnow()

    db_object = UnstructuredORM(**object_dict)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)

    logging.info(f"Adding unstructured with id={db_object.id} to vectorstore...")
    vectorstore_id = unstructured_orm_to_vectorstore(db_object)
    db_object.vectorstore_id = vectorstore_id
    db.commit()

    return db_object
