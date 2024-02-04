import logging

from langchain_community.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.orm import Session

from app.constants import COHERE_API_KEY, COHERE_CHAT_MODEL
from app.db.models import DataframeORM, ValueORM, VariableORM
from app.db.services import get_object_by_id
from app.db.vectorstore import get_vectorstore
from app.push.prompts import SYSTEM_PROMPT


class PushAgent:
    _NUM_SEARCHED_DOCS = 3

    def __init__(self, db: Session) -> None:
        self.db = db
        self.vectorstore = get_vectorstore()

    def _get_context(self, user_query: str) -> str:
        searched_docs = self.vectorstore.similarity_search(
            user_query, k=self._NUM_SEARCHED_DOCS
        )

        available_orms = {
            orm.__name__: orm for orm in [DataframeORM, VariableORM, ValueORM]
        }
        doc_descriptions = []
        for doc in searched_docs:
            orm_type = doc.metadata["type"]
            db_obj = get_object_by_id(
                db=self.db,
                orm=available_orms[orm_type],
                id=doc.metadata["id"],
            )
            doc_descriptions.append(
                f"Type: {orm_type[:-3]}\nName: {db_obj.name}.\nDescription: {db_obj.description}"
            )

        return "\n-----\n".join(doc_descriptions)

    def run(self, user_query: str, chat_conversation: list[tuple[str, str]]) -> str:
        logging.info(f"Running push agent with user query: {user_query}")
        llm = ChatCohere(cohere_api_key=COHERE_API_KEY, model=COHERE_CHAT_MODEL)
        prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT)]
            + chat_conversation
            + [("human", "{user_query}")]
        )
        chain = prompt | llm

        context = self._get_context(user_query)
        logging.info(f"Using context:\n{context}")

        response = chain.invoke({"user_query": user_query, "context": context})
        return response.content
