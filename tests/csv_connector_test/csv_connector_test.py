import logging
import os.path

from app.connectors.csv_connector import CSVConnector

logging.basicConfig(level=logging.INFO)

path = os.path.abspath("biostats.csv")
return_data = {
    "db_name": "DB on biostats",
    "db_description": "DB on biostats",
    "Name": "Name of the user",
    "Sex": "Sex of the user",
    "Age": "Age of the user",
    "Height (in)": "Height of the user",
    "Weight (lbs)": "Weight of the user",
    "M": "Man",
    "F": "Women",
}
name = "DB on biostats"
descr = "DB on biostats"

csvconn = CSVConnector(path)

specifications = csvconn.get_specifications()
print(specifications)
# csvconn.save_data(data_dict=return_data)
# print(csvconn.get_data_info())
# print(csvconn.get_data_content())

# csvconn.upload_data(db=None)
