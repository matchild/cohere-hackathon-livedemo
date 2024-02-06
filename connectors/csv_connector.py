import csv

import pandas as pd

from app.db import Base
from app.db.db import engine, SessionLocal
from app.db.schemas import DataframeFull, VariableFull
from app.db.services import register_full_dataframe

Base.metadata.create_all(bind=engine)
db = SessionLocal()


class CSVConnector:
    def __init__(self, file):
        self.columns_description = {}
        self.categorical_values_description = {}
        self.db_description = None
        self.db_name = None

        self.input_df = pd.read_csv(file)
        self.column_names = self.input_df.columns.tolist()
        self.content = self.input_df.values.tolist()
        self.categorical_values = self.check_categoricals()

    def save_data(self, data_dict: dict):
        self.db_name = data_dict.pop("db_name")
        self.db_description = data_dict.pop("db_description")
        for column in self.column_names:
            self.columns_description[column] = data_dict[column]
            for cat_value in self.categorical_values.get(column, []):
                self.categorical_values_description[cat_value] = data_dict[cat_value]
        self.check_columns()

    def check_columns(self):
        if not self.column_names:
            raise Exception("No header")
        elif not set(list(self.columns_description.keys())) == set(self.column_names):
            print(set(list(self.columns_description.keys())))
            print(set(self.column_names))
            raise Exception("Column description not correct")

    def get_data_content(self) -> list:
        return self.content

    def get_data_info(self) -> dict:
        response = {
            "name": self.db_name,
            "description": self.db_description,
            "columns": self.column_names,
            "columns_description": self.columns_description,
            "categorical_values_description": self.categorical_values_description
        }
        return response

    def get_specifications(self) -> dict:
        columns_prompts = []
        cat_values_prompts = []
        cat_values_flat = []
        for column_name in self.column_names:
            columns_prompts.append("Describe the column " + column_name + " of the dataset you just uploaded")
            for cat_value in self.categorical_values.get(column_name, []):
                columns_prompts.append(
                    "Describe the meaning of categorical value " + cat_value + " for column " + column_name + " of the dataset you just uploaded")
                cat_values_flat.append(cat_value)
        specs = {
            "inputs_required": ["db_name", "db_description"] + self.column_names + cat_values_flat,
            "inputs_required_prompts": ["Give a short name to the data you just uploaded",
                                        "Describe the data you just uploaded"] + columns_prompts + cat_values_prompts
        }
        return specs

    def check_categoricals(self):
        categorical_values = {}
        categorical_df = self.input_df.select_dtypes(include=['category', 'object'])
        columns_categorical = categorical_df.columns.tolist()
        for column in columns_categorical:
            if categorical_df[column].nunique() < 5:
                categorical_values[column] = categorical_df[column].unique().tolist()
        return categorical_values

    def upload_data(self):
        pass
