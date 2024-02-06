import csv


class CSVConnector:
    def __init__(self, file_path, name, columns_description):
        self.file = open(file_path)
        self.csv_reader = csv.reader(self.file)
        self.name = name
        self.columns_description = columns_description
        self.column_names = self.column_names_extractor()
        self.content = None
        self.description = None

    def column_names_extractor(self):
        header = next(self.csv_reader)
        if not header:
            raise Exception("No header")
        elif not set(list(self.columns_description.keys())) == set(self.column_names):
            raise Exception("Column description not correct")
        else:
            return header

    def ask_name(self):
        pass
