import logging

import cohere
from sqlalchemy.orm import Session

from app.constants import COHERE_API_KEY
from app.db.models import DataframeORM, ValueORM, VariableORM
from app.db.services import get_object_by_id
from app.db.vectorstore import get_vectorstore


class PushAgent:
    _NUM_SEARCHED_DOCS = 3
    _available_orms = {
        orm.__name__: orm for orm in [DataframeORM, VariableORM, ValueORM]
    }

    def __init__(self, db: Session) -> None:
        self.db = db
        self.vectorstore = get_vectorstore()

    def _retrieve_docs(self, search_queries: list[str]) -> list[dict[str, str]]:
        """Get the relevant documents through a similarity search in the vectorstore"""
        retrieved_docs = []
        for search_query in search_queries:
            logging.info(f"Performing vector search with query: {search_query}")
            search_docs = self.vectorstore.similarity_search(
                search_query["text"], k=self._NUM_SEARCHED_DOCS
            )
            for doc in search_docs:
                orm_type = doc.metadata["type"]
                db_obj = get_object_by_id(
                    db=self.db,
                    orm=self._available_orms[orm_type],
                    id=doc.metadata["id"],
                )

                retrieved_docs.append(
                    {
                        "type": orm_type[:-3],
                        "name": db_obj.name,
                        "description": db_obj.description,
                    }
                )

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
