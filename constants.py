import os

from dotenv import load_dotenv

load_dotenv(override=True)

COHERE_API_KEY = os.environ["COHERE_API_KEY"]
COHERE_MODEL = "command"
