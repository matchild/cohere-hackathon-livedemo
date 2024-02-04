from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from app.constants import CHROMA_FOLDER, COHERE_API_KEY, COHERE_EMBEDDING_MODEL


def get_vectorstore() -> Chroma:
    return Chroma(
        persist_directory=CHROMA_FOLDER,
        embedding_function=CohereEmbeddings(
            cohere_api_key=COHERE_API_KEY, model=COHERE_EMBEDDING_MODEL
        ),
    )


# add document test
# from langchain_core.documents import Document

# test_doc = Document(page_content="This is a test document.")
# vectorstore = get_vectorstore()
# res = vectorstore.add_documents([test_doc])
