import logging

import cohere
from sqlalchemy.orm import Session

from app.constants import COHERE_API_KEY
from app.db.vectorstore import get_vectorstore


class PullAgent:
    _QUESTION_PROMPT = 'You will receive a request that starts with the tag "REQUEST:" followed by the request.' \
                       'The request is about some data that the user gave as input. ' \
                       'Your goal is to reformulate the request to improve it. ' \
                       'The user is the expert this piece of data, so be specific. ' \
                       'You can give hypotheses about what you think the request is about.' \
                       'Remember that you have to bring the user to be as precise and complete as possible. ' \
                       'Please keep the rephrased sentence concise and ' \
                       'do not change the name of the variables contained in the request. ' \
                       'Give in output only the rephrased request, without the tag "REQUEST:" and anything else'

    def run(self, data_specification_request: str) -> str:
        logging.info(f"Running push agent with user query: {data_specification_request}")
        co = cohere.Client(COHERE_API_KEY)

        complete_prompt = self._QUESTION_PROMPT + " REQUEST: " + data_specification_request

        # generate search queries
        response = co.generate(
            prompt=complete_prompt
        )
        print(response)
        return response[0].text
