import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class DataframeORM(Base):
    __tablename__ = "dataframes"

    id: Mapped[int] = mapped_column(primary_key=True)
    vectorstore_id: Mapped[Optional[str]]
    name: Mapped[str]
    description: Mapped[str]
    registered_at: Mapped[datetime.datetime]

    variables: Mapped[list["VariableORM"]] = relationship(back_populates="dataframe")

    def __repr__(self) -> str:
        return f"DataframeORM(id={self.id!r}, name={self.name!r})"


class VariableORM(Base):
    __tablename__ = "variables"

    id: Mapped[int] = mapped_column(primary_key=True)
    vectorstore_id: Mapped[Optional[str]]
    dataframe_id: Mapped[int] = mapped_column(ForeignKey("dataframes.id"))
    name: Mapped[str]
    description: Mapped[str]
    is_categorical: Mapped[bool]
    registered_at: Mapped[datetime.datetime]

    dataframe: Mapped["DataframeORM"] = relationship(back_populates="variables")
    values: Mapped[list["ValueORM"]] = relationship(back_populates="variable")

    def __repr__(self) -> str:
        return f"VariableORM(id={self.id!r}, name={self.name!r})"


class ValueORM(Base):
    __tablename__ = "values"

    id: Mapped[int] = mapped_column(primary_key=True)
    vectorstore_id: Mapped[Optional[str]]
    variable_id: Mapped[int] = mapped_column(ForeignKey("variables.id"))
    name: Mapped[str]
    description: Mapped[str]
    registered_at: Mapped[datetime.datetime]

    variable: Mapped["VariableORM"] = relationship(back_populates="values")

    def __repr__(self) -> str:
        return f"ValueORM(id={self.id!r}, name={self.name!r})"
