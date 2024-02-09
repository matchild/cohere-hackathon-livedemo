import logging

import cohere

from app.constants import COHERE_API_KEY


class PullAgent:
    _PROMPT_REPHRASING = (
        "Given the following request, generate a revised version that better fits into the conversation. "
        "You are talking to a data expert who uploaded some data. "
        "Your goal is to collect additional information throughout the conversation. "
        "Ask only about the request you receive but use the memory to ask more meaningful questions."
        "Do not aks about previous requests."
        "Do not add any information that is not strictly related to the request in your revised request. "
        "Use the following format: {key}."
        "Request: {request}"
    )
    _PROMPT_FORMULATING = (
        "Given the following request, generate one question about the data mentioned in the conversation. "
        "You are talking to a data expert who uploaded some data. "
        "Your goal is to collect additional information throughout the conversation. "
        "Do not ask something that was asked before but you can ask clarifying questions. "
        "If you're are asking a clarifying question, specify it and mention what led to this questions. "
        "You can also ask questions about some information you think are missing but important to understand "
        "the data uploaded by the user. "
        "Use the following format: {key}."
    )
    _KEY = "Revised request"

    def run_rephrasing(
        self, request: str, chat_history: list[dict[str, str]] = []
    ) -> str:
        logging.info(f"Running pull agent with rephrasing request: {request}")

        co = cohere.Client(COHERE_API_KEY)
        response = co.chat(
            message=self._PROMPT_REPHRASING.format(key=self._KEY, request=request),
            chat_history=chat_history,
        )

        full_key = f"{self._KEY}: "
        if response.text[: len(full_key)] == full_key:
            return response.text[len(full_key) :]

        return response.text

    def run_formulating(self, chat_history: list[dict[str, str]] = []) -> str:
        logging.info(f"Running pull agent with formulating request")

        co = cohere.Client(COHERE_API_KEY)
        response = co.chat(
            message=self._PROMPT_FORMULATING.format(key=self._KEY),
            chat_history=chat_history,
        )

        full_key = f"{self._KEY}: "
        if response.text[: len(full_key)] == full_key:
            return response.text[len(full_key) :]

        return response.text
