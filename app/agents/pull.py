import logging

import cohere
from cohere.responses.classify import Example

from app.constants import COHERE_API_KEY


def chat_to_text(chat_history: list[dict[str, str]] = []) -> str:
    chat_string = ""
    for chat_elem in chat_history[:-1]:
        chat_string += str(chat_elem["role"]) + ": " + str(chat_elem["message"] + "\n")
    return chat_string


class PullAgent:
    _PROMPT_REPHRASING = (
        "Given the following request, generate a revised version that better fits into the conversation. "
        "You are talking to a data owner who uploaded some data. "
        "Your goal is to reframe the questions you received in input to "
        "collect additional information about the data and its use in the organization."
        "Ask only about the request you receive but use the memory to ask more meaningful questions."
        "Do not aks about previous requests and do mention previous columns."
        "Do not add any information that is not strictly related to the request in your revised request. "
        "Use the following format at the beginning of each answer: {key}."
        "Do not add any other key in your answer."
        "Keep it concise, around 1 or 2 sentences maximum"
        "Request: {request}"
    )
    _PROMPT_FORMULATING = (
        "Given the following request, generate one question about the data mentioned in the conversation. "
        "You are talking to a data owner who uploaded some data. "
        "Your goal is to collect additional information such as:"
        "- What is this data used for?"
        "- Is it based on other sources or inputs?"
        "- How often this data is updated?"
        "Do not ask something that was asked before but you can ask clarifying questions. "
        "Use the following format at the beginning of each answer: {key}."
        "Do not add any other key in your answer."
        "Keep it concise, around 1 or 2 sentences maximum"
    )
    _KEY = "REVISED REQUEST"

    _CLASSIFY_REPLY = "Answer reply"
    _CLASSIFY_CLARIFICATION = "Clarification question"

    _EXAMPLES_CLASSIFY = [
        Example("Sure, the sensitivity of data refers to how critical or confidential the information is",
                _CLASSIFY_REPLY),
        Example(
            "Could you specify the type of data you're referring to? Are you asking about personal information, "
            "financial records, or something else?",
            _CLASSIFY_CLARIFICATION),
        Example("Certainly, the 'Index' column typically serves as a unique identifier for each entry in the dataset",
                _CLASSIFY_REPLY),
        Example(
            "Could you specify the specific dataset you're referring to? Is it a sales dataset, a customer database, "
            "or another type of data?",
            _CLASSIFY_CLARIFICATION),
        Example("The data represents transaction details such as date, product sold, quantity, and revenue",
                _CLASSIFY_REPLY),
        Example("Could you provide more context or specify which dataset you're referring to?",
                _CLASSIFY_CLARIFICATION),
        Example("You can ignore this column, it is not useful", _CLASSIFY_REPLY),
        Example("I don't understand the question", _CLASSIFY_CLARIFICATION),
        Example("Customers data", _CLASSIFY_REPLY),
        Example("In 2023", _CLASSIFY_REPLY),
        Example("Describes how the system works", _CLASSIFY_REPLY),
    ]

    _PROMPT_SUMMARIZING = (
        "Take the main key messages from the chat between user and AI about a specific file. "
        "Focus on reporting the variables given so far and their meaning in a schematic way."
        "Use third person indirect sentences and do not mention user and AI."
    )

    _PROMPT_CREATE_DESCRIPTION = (
        "Given multiple source of inputs, merge the information to have a single description. "
        "Do not invent anything and stick to content present in the sources. "
        "You can rephrase and adjust the text, if needed "
        "Information: {info}"
    )

    def run_rephrasing(
            self, request: str, chat_history: list[dict[str, str]] = []
    ) -> str:
        logging.info(f"Running pull agent with rephrasing request: {request}")

        co = cohere.Client(COHERE_API_KEY)
        response = co.chat(
            message=self._PROMPT_REPHRASING.format(key=self._KEY, request=request),
            chat_history=chat_history,
        )

        full_key_with_colon = f"{self._KEY}: "
        full_key_without_colon = f"{self._KEY} "
        if response.text[: len(full_key_with_colon)] == full_key_with_colon:
            return response.text[len(full_key_with_colon):]
        if response.text[: len(full_key_without_colon)] == full_key_without_colon:
            return response.text[len(full_key_without_colon):]

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
            return response.text[len(full_key):]

        return response.text

    def is_run_classifying_ok(self, response: str) -> bool:
        co = cohere.Client(COHERE_API_KEY)
        response = co.classify(
            inputs=[response],
            examples=self._EXAMPLES_CLASSIFY
        )
        response_string = response[0].predictions[0]
        logging.info(f"Running classifying agent with user response, classified as {response_string}")
        return True if response_string == self._CLASSIFY_REPLY else False

    def summarize_chat(self, chat_history: list[dict[str, str]] = []) -> str:
        response = ""

        chat_text = chat_to_text(chat_history)
        if len(chat_text) > 300:
            logging.info(f"Summarizing agent based on chat")
            co = cohere.Client(COHERE_API_KEY)
            response = co.summarize(
                text=chat_to_text(chat_history),
                additional_command=self._PROMPT_SUMMARIZING
            ).summary
        return response

    def create_description(self, inputs: str) -> str:
        logging.info(f"Creating unified description based on the questions asked")
        co = cohere.Client(COHERE_API_KEY)
        response = co.generate(
            prompt=self._PROMPT_CREATE_DESCRIPTION.format(info=inputs)
        ).generations[0].text
        return response
