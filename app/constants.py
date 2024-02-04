import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Cohere
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
COHERE_CHAT_MODEL = "command"
COHERE_EMBEDDING_MODEL = "embed-english-light-v3.0"

# Database
DATA_FOLDER = "./data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
SQL_DATABASE_URL = f"sqlite:///{DATA_FOLDER}/test.db"
CHROMA_FOLDER = f"{DATA_FOLDER}/chroma_db"
