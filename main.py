import cohere
from langchain_community.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate

from constants import COHERE_API_KEY, COHERE_MODEL

MESSAGE = "Hello world!"
SYSTEM_PROMPT = "You are a helpful assistant"

# Langchain API
llm = ChatCohere(model=COHERE_MODEL)
prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", "{message}")])
chain = prompt | llm
response = chain.invoke({"message": MESSAGE})
print(response.content)


# Cohere API
co = cohere.Client(COHERE_API_KEY)
response = co.chat(message=MESSAGE, chat_history=[], connectors=[], model=COHERE_MODEL)
print(response.text)
