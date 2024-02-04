import os

from dotenv import load_dotenv

load_dotenv(override=True)

COHERE_API_KEY = os.environ["COHERE_API_KEY"]
COHERE_CHAT_MODEL = "command"
COHERE_EMBEDDING_MODEL = "embed-english-light-v3.0"

CHROMA_FOLDER = "./data/chroma_db"
