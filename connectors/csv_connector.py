import csv


class CSVConnector:
    def __init__(self, file_path):
        self.columns_description = None
        self.description = None
        self.name = None

        self.file = open(file_path)
        self.csv_reader = csv.reader(self.file)
        self.column_names = self.column_names_extractor()
        self.content = self.read_content()

    def save_data(self, name, columns_description, db_description):
        self.name = name
        self.description = db_description
        self.columns_description = columns_description
        self.check_columns()

    def check_columns(self):
        if not self.column_names:
            raise Exception("No header")
        elif not set(list(self.columns_description.keys())) == set(self.column_names):
            print(set(list(self.columns_description.keys())))
            print(set(self.column_names))
            raise Exception("Column description not correct")

    def column_names_extractor(self):
        header = next(self.csv_reader)
        return header

    def read_content(self):
        rows = []
        for row in self.csv_reader:
            rows.append(row)
        return rows

    def get_data_content(self):
        return self.content

    def get_data_info(self):
        response = {
            "name": self.name,
            "description": self.description,
            "columns": self.column_names,
            "columns_description": self.columns_description
        }
        return response

    def get_specifications(self):
        specs = {
            "inputs_required": ["name", "db_description", "columns_description"],
            "inputs_required_prompts": ["Give a short name to the data you just uploaded",
                                        "Describe the data you just uploaded",
                                        "Describe the columns of the dataset you just uploaded"],
            "additional_data": {"column_names": self.column_names}
        }
        return specs
