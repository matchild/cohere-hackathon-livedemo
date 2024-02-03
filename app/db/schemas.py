import datetime

from pydantic import BaseModel


# Dataframe
class Dataframe(BaseModel):
    name: str
    description: str


class DataframeInDB(Dataframe):
    id: int
    registered_at: datetime.datetime

    class Config:
        from_attributes = True


# Variable
class Variable(BaseModel):
    dataframe_id: int
    name: str
    description: str
    is_categorical: bool


class VariableInDB(Variable):
    id: int
    registered_at: datetime.datetime

    class Config:
        from_attributes = True


# Value
class Value(BaseModel):
    variable_id: int
    name: str
    description: str


class ValueInDB(Variable):
    id: int
    registered_at: datetime.datetime

    class Config:
        from_attributes = True
