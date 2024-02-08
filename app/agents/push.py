import logging

import cohere
from sqlalchemy.orm import Session

from app.constants import COHERE_API_KEY
from app.db.models import DataframeORM, UnstructuredORM, ValueORM, VariableORM
from app.db.services import (
    get_dataframe_by_id,
    get_unstructured_by_id,
    get_value_by_id,
    get_variable_by_id,
)
from app.db.vectorstore import get_vectorstore


class AiAgent:
    _NUM_SEARCHED_DOCS = 3
    _available_orms = {
        orm.__name__: orm
        for orm in [DataframeORM, VariableORM, ValueORM, UnstructuredORM]
    }

    def __init__(self, db: Session) -> None:
        self.db = db
        self.vectorstore = get_vectorstore()

    def _db_object_to_doc(self, orm_type: str, object_id: int) -> dict[str, str]:
        if orm_type == DataframeORM.__name__:
            db_dataframe = get_dataframe_by_id(db=self.db, id=object_id)
            return {
                "dataframe_name": db_dataframe.name,
                "dataframe_description": db_dataframe.description,
            }

        elif orm_type == VariableORM.__name__:
            db_variable = get_variable_by_id(db=self.db, id=object_id)
            return {
                "dataframe_name": db_variable.dataframe.name,
                "dataframe_description": db_variable.dataframe.description,
                "variable_name": db_variable.name,
                "variable_description": db_variable.description,
            }

        elif orm_type == ValueORM.__name__:
            db_value = get_value_by_id(db=self.db, id=object_id)
            return {
                "dataframe_name": db_value.variable.dataframe.name,
                "dataframe_description": db_value.variable.dataframe.description,
                "variable_name": db_value.variable.name,
                "variable_description": db_value.variable.description,
                "value_name": db_value.name,
                "value_description": db_value.description,
            }

        elif orm_type == UnstructuredORM.__name__:
            db_unstructured = get_unstructured_by_id(db=self.db, id=object_id)
            return {
                "file_name": db_unstructured.name,
                "file_description": db_unstructured.description,
                "file_content": db_unstructured.content,
            }

        else:
            raise Exception(f"ORM type not accepted: {orm_type}")

    def _retrieve_docs(self, search_queries: list[str]) -> list[dict[str, str]]:
        """Get the relevant documents through a similarity search in the vectorstore"""
        retrieved_docs = []
        used_object_ids = {n: [] for n in self._available_orms.keys()}
        for search_query in search_queries:
            logging.info(f"Performing vector search with query: {search_query}")
            search_docs = self.vectorstore.similarity_search(
                search_query["text"], k=self._NUM_SEARCHED_DOCS
            )

            for doc in search_docs:
                orm_type = doc.metadata["type"]
                id = doc.metadata["id"]
                if id not in used_object_ids[orm_type]:
                    rendered_doc = self._db_object_to_doc(
                        orm_type=orm_type, object_id=id
                    )
                    used_object_ids[orm_type].append(id)
                    retrieved_docs.append(rendered_doc)

        return retrieved_docs

    def run(self, user_query: str, chat_history: list[dict[str, str]]) -> str:
        logging.info(f"Running push agent with user query: {user_query}")
        co = cohere.Client(COHERE_API_KEY)

        # generate search queries
        response = co.chat(
            message=user_query, chat_history=chat_history, search_queries_only=True
        )

        if response.search_queries:
            # RAG response
            retrieved_docs = self._retrieve_docs(response.search_queries)
            response = co.chat(
                message=user_query, chat_history=chat_history, documents=retrieved_docs
            )

        else:
            # direct LLM response
            response = co.chat(message=user_query, chat_history=chat_history)

        return response.text
