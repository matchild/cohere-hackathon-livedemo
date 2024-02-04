import datetime

from pydantic import BaseModel


# Value
class ValueLone(BaseModel):
    name: str
    description: str


class Value(ValueLone):
    variable_id: int


class ValueInDB(Value):
    id: int
    vectorstore_id: str
    registered_at: datetime.datetime

    class Config:
        from_attributes = True


# Variable
class VariableLone(BaseModel):
    name: str
    description: str
    is_categorical: bool


class Variable(VariableLone):
    dataframe_id: int


class VariableFull(VariableLone):
    values: list[ValueLone]


class VariableInDB(Variable):
    id: int
    vectorstore_id: str
    registered_at: datetime.datetime

    class Config:
        from_attributes = True


# Dataframe
class Dataframe(BaseModel):
    name: str
    description: str


class DataframeFull(Dataframe):
    variables: list[VariableFull]


class DataframeInDB(Dataframe):
    id: int
    vectorstore_id: str
    registered_at: datetime.datetime

    class Config:
        from_attributes = True
