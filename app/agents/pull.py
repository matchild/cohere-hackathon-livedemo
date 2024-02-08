import logging

import cohere

from app.constants import COHERE_API_KEY


class PullAgent:
    _PROMPT = (
        "Given the following request, generate a revised version that better fits into the conversation. "
        "You are talking to a data expert who uploaded some data. "
        "Your goal is to collect additional information throughout the conversation. "
        "Use the following format: Revised request."
        "Request: {request}"
    )

    def run(self, request: str, chat_history: list[dict[str, str]] = []) -> str:
        logging.info(f"Running pull agent with request: {request}")

        co = cohere.Client(COHERE_API_KEY)
        response = co.chat(
            message=self._PROMPT.format(request=request), chat_history=chat_history
        )

        if response.text[:17] == "Revised request: ":
            return response.text[16:]

        return response.text
