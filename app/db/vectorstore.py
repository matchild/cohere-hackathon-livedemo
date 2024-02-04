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


# Test
from langchain_core.documents import Document

# CONTRACTS dataframe
test_doc_dataframe1 = Document(page_content="This table contains all the information related to the active contracts the company has with its customers",
                           metadata={"type": "dataframe",
                                     "dataframe_id": 1})
# CONTRACTS variables
test_doc_variables1 = Document(page_content="Type of contract defining the commodity, market segment and branch of the company who issued the contract",
                               metadata={"type": "variable" ,
                                         "table_id": 1,
                                         "variable_id": 2})
# CUSTOMERS dataframe
test_doc_dataframe2 = Document(page_content="This table contains all the information related to the customers",
                           metadata={"type": "dataframe",
                                     "dataframe_id": 2})


vectorstore = get_vectorstore()
res = vectorstore.add_documents([test_doc_dataframe1, test_doc_variables1, test_doc_dataframe2])


vectorstore.similarity_search_with_score(
    query="data about clients",
    k=1,
    filter={"type": "dataframe"},
)