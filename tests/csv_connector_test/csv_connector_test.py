import os.path

from connectors.csv_connector import CSVConnector

path = os.path.abspath("biostats.csv")
columns = {
    "Name": "Name of the user",
    "Sex": "Sex of the user",
    "Age": "Age of the user",
    "Height (in)": "Height of the user",
    "Weight (lbs)": "Weight of the user"
}
name = "DB on biostats"
descr = "DB on biostats"

csvconn = CSVConnector(path)

print(csvconn.get_specifications())
csvconn.save_data(name=name, db_description=descr, columns_description=columns)
print(csvconn.get_data_info())
print(csvconn.get_data_content())
