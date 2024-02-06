from pypdf import PdfReader

class PDFConnector:
    def __init__(self, file_path):
        self.description = None
        self.name = None

        self.reader = PdfReader(file_path)
        self.content = self.read_content()

    def save_data(self, name, file_description):
        self.name = name
        self.description = file_description

    def read_content(self):
        text = ""
        for page in self.reader.pages:
            text += page.extract_text() + "\n"
        return text

    def get_data_content(self):
        return self.content

    def get_data_info(self):
        response = {
            "name": self.name,
            "description": self.description
        }
        return response

    def get_specifications(self):
        specs = {
            "inputs_required": ["name", "file_description"],
            "inputs_required_prompts": ["Give a short name to the data you just uploaded",
                                        "Describe the file you just uploaded"],
            "additional_data": None
        }
        return specs
