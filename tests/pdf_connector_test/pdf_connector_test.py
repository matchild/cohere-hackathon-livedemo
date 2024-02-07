import os.path

from app.connectors.pdf_connector import PDFConnector

path = os.path.abspath("bitcoin.pdf")
name = "Bitcoin"
descr = "Bitcoin Paper"

pdfconn = PDFConnector(path)

# print(pdfconn.get_specifications())
pdfconn.save_data(name=name, file_description=descr)
print(pdfconn.get_data_info())
# print(pdfconn.get_data_content())
