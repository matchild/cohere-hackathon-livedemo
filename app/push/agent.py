from langchain_community.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate

from app.constants import COHERE_MODEL
from app.push.prompts import SYSTEM_PROMPT


def run(user_query: str, chat_conversation: list[tuple[str, str]]) -> str:
    llm = ChatCohere(model=COHERE_MODEL)
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT)] + chat_conversation + [("human", "{user_query}")]
    )
    chain = prompt | llm

    response = chain.invoke({"user_query": user_query})
    return response.content
