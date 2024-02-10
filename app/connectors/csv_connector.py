import logging

import pandas as pd
from sqlalchemy.orm import Session

from app.agents.pull import PullAgent
from app.db.schemas import (
    DataframeFull,
    DataframeInDB,
    ValueInDB,
    ValueLone,
    VariableFull,
    VariableInDB,
)
from app.db.services import register_full_dataframe


class CSVConnector:
    _CATEGORICAL_THRESHOLD = 5

    def __init__(self, file) -> None:
        self.columns_description = {}
        self.categorical_values_description = {}
        self.db_description = None
        self.db_name = None

        self.input_df = pd.read_csv(file)
        self.column_names = self.input_df.columns.tolist()
        self.content = self.input_df.values.tolist()
        self.categorical_values = self.check_categoricals()

    def save_data(self, data_list: dict[str, dict[str, str]]) -> None:
        data_required = data_list['required']
        data_additional = data_list["additional"]
        self.db_name = data_required.pop("db_name")
        for column in self.column_names:
            self.columns_description[column] = data_required[column]
            for cat_value in self.categorical_values.get(column, []):
                self.categorical_values_description[cat_value] = data_required[cat_value]

        additional_info = ""
        for (additional_elem_key, additional_elem_value) in data_additional.items():
            additional_info += f"{additional_elem_key}: {additional_elem_value} /n"
        additional_info += data_required['db_description']
        self.db_description = PullAgent().create_description(additional_info)

    def check_columns(self) -> bool:
        if not self.column_names:
            raise Exception("No header")
        elif not set(list(self.columns_description.keys())) == set(self.column_names):
            logging.info(set(list(self.columns_description.keys())))
            logging.info(set(self.column_names))
            raise Exception("Column description not correct")

    def get_data_content(self) -> list:
        return self.content

    def get_data_info(self) -> dict:
        response = {
            "name": self.db_name,
            "description": self.db_description,
            "columns": self.column_names,
            "columns_description": self.columns_description,
            "categorical_values_description": self.categorical_values_description,
        }
        return response

    def get_specifications(self) -> dict:
        columns_prompts = []
        cat_values_prompts = []
        cat_values_flat = []
        for column_name in self.column_names:
            columns_prompts.append(
                "Describe the column '"
                + column_name
                + "' of the dataset you just uploaded."
            )
            for cat_value in self.categorical_values.get(column_name, []):
                cat_values_prompts.append(
                    "Describe the meaning of categorical value '"
                    + cat_value
                    + "' for column '"
                    + column_name
                    + "' of the dataset you just uploaded."
                )
                cat_values_flat.append(cat_value)
        specs = {
            "inputs_required": ["db_name", "db_description"]
            + self.column_names
            + cat_values_flat,
            "inputs_required_prompts": [
                "Please, provide a short but significant name to the dataset you just uploaded.",
                "Provide a detailed description of the usage of the dataset you just uploaded.",
            ]
            + columns_prompts
            + cat_values_prompts,
        }
        return specs

    def check_categoricals(self) -> dict[str, str]:
        categorical_values = {}
        categorical_df = self.input_df.select_dtypes(include=["category", "object"])
        columns_categorical = categorical_df.columns.tolist()
        for column in columns_categorical:
            if categorical_df[column].nunique() < self._CATEGORICAL_THRESHOLD:
                categorical_values[column] = categorical_df[column].unique().tolist()
        return categorical_values

    def upload_data(
        self, db: Session | None
    ) -> list[DataframeInDB | VariableInDB | ValueInDB] | None:
        self.check_columns()
        if self.db_name is None or self.db_description is None:
            raise Exception("Cannot upload data to database with missing information")

        variables = []
        for col in self.column_names:
            values = []
            is_categorical = col in self.categorical_values.keys()
            if is_categorical:
                for val in self.categorical_values[col]:
                    values.append(
                        ValueLone(
                            name=val,
                            description=self.categorical_values_description[val],
                        )
                    )
            variables.append(
                VariableFull(
                    name=col,
                    description=self.columns_description[col],
                    is_categorical=is_categorical,
                    values=values,
                )
            )
        dataframe = DataframeFull(
            name=self.db_name, description=self.db_description, variables=variables
        )

        logging.info(f"Uploading CSV to SQL database: {dataframe}")
        if db is not None:
            return register_full_dataframe(db, dataframe)
