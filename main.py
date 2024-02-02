import cohere
from langchain_community.chat_models import ChatCohere

from constants import COHERE_API_KEY, COHERE_MODEL

MESSAGE = "Hello world!"

# Langchain API
llm = ChatCohere(model=COHERE_MODEL)
response = llm.invoke(MESSAGE)
print(response.content)


# Cohere API
co = cohere.Client(COHERE_API_KEY)
response = co.chat(message=MESSAGE, chat_history=[], connectors=[], model=COHERE_MODEL)
print(response.text)
