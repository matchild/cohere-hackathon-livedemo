import logging

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.agents.pull import PullAgent
from app.db.schemas import Unstructured, UnstructuredInDB
from app.db.services import register_unstructured
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFConnector:
    def __init__(self, file_path) -> None:
        self.file_name = None
        self.file_description = None

        self.reader = PdfReader(file_path)
        self.content = self.read_content()

    def save_data(self, data_list: dict[str, dict[str, str]]) -> None:
        print(data_list)
        data_required = data_list['required']
        data_additional = data_list["additional"]
        self.file_name = data_required['file_name']

        additional_info = ""
        for (additional_elem_key, additional_elem_value) in data_additional.items():
            additional_info += f"{additional_elem_key}: {additional_elem_value} /n"
        additional_info += data_required['file_description']
        self.file_description = PullAgent().create_description(additional_info)

    def read_content(self) -> str:
        text = ""
        for page in self.reader.pages:
            text += page.extract_text() + "\n"
        return text

    def get_data_content(self) -> str:
        return self.content

    def get_data_info(self) -> dict[str, str]:
        response = {
            "file_name": self.file_name,
            "file_description": self.file_description,
        }
        return response

    def get_specifications(self) -> dict[str, list[str]]:
        specs = {
            "inputs_required": ["file_name", "file_description"],
            "inputs_required_prompts": [
                "Please, provide a short but significant name to the file you just uploaded.",
                "Provide a detailed description of the usage of the file you just uploaded.",
            ],
        }
        return specs

    def upload_data(self, db: Session | None) -> list[UnstructuredInDB] | None:
        if self.file_name is None or self.file_description is None:
            raise Exception("Cannot upload data to database with missing information")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        text_splits = text_splitter.split_text(self.content)
        return_chunks = []
        for count, split in enumerate(text_splits):
            unstructured = Unstructured(
                name=self.file_name, description=self.file_description, content=split
            )

            logging.info(f"Uploading PDF to database: {count}")
            if db is not None:
                db_object = register_unstructured(db, unstructured)
                return_chunks.append(UnstructuredInDB.model_validate(db_object))
        return return_chunks

