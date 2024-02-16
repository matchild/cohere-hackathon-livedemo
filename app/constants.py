import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Cohere
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
COHERE_EMBEDDING_MODEL = "embed-english-v3.0"


# Database
DATA_FOLDER = "./data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
SQL_DATABASE_URL = f"sqlite:///{DATA_FOLDER}/test.db"

# Vectorstore
USE_LOCAL_VECTORSTORE = True

# Chroma: local
CHROMA_FOLDER = f"{DATA_FOLDER}/chroma_db"

# Pinecone: live
# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_API_KEY = "NA"
PINECONE_INDEX = "cohere-hackathon"
