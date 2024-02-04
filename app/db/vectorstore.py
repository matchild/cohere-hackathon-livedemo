import os

from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document

from app.constants import CHROMA_FOLDER, COHERE_API_KEY, COHERE_EMBEDDING_MODEL
from app.db import DataframeORM, ValueORM, VariableORM


def get_vectorstore() -> Chroma:
    if not os.path.exists(CHROMA_FOLDER):
        os.makedirs(CHROMA_FOLDER)

    return Chroma(
        persist_directory=CHROMA_FOLDER,
        embedding_function=CohereEmbeddings(
            cohere_api_key=COHERE_API_KEY, model=COHERE_EMBEDDING_MODEL
        ),
    )


def add_to_vectorstore(orm: DataframeORM | VariableORM | ValueORM) -> str:
    vectorstore = get_vectorstore()

    page_content = f"{orm.name}\n{orm.description}"
    doc = Document(
        page_content=page_content,
        metadata={"id": orm.id, "type": type(orm).__name__},
    )

    res = vectorstore.add_documents([doc])
    return res[0]
