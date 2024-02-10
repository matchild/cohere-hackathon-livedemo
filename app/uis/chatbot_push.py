import random

import streamlit as st

from app.agents.push import AiAgent
from app.uis.utils import st_chat_containers


def _color_string(string: str, start: int, end: int) -> tuple[str, str]:
    _COLOR_OPTIONS = ["blue", "green", "orange", "red", "violet"]
    color = random.choice(_COLOR_OPTIONS)
    colored_string = f":{color}[{string[start:end]}]"
    return (string[:start] + colored_string + string[end:], color)


def chat_ui_push() -> None:
    """Chatbot UI for push chat"""

    if "init_push" not in st.session_state:
        st.session_state["init_push"] = True
        st.session_state["messages_push"] = []
        st.session_state["cited_docs"] = []

    st.title("Retrieval Chat 📬")

    container1, container2, user_query = st_chat_containers("Chat", "Citations")

    with container1:
        for message in st.session_state["messages_push"]:
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

        if user_query:
            st.chat_message("user").markdown(user_query)

            with st.spinner("Thinking..."):
                with st.session_state["conn"].session as db_session:
                    agent = AiAgent(db=db_session)
                    ai_answer, citations, rag_docs = agent.run(
                        user_query, chat_history=st.session_state["messages_push"]
                    )
                    st.session_state["cited_docs"] = []
                    if citations is not None and len(citations):
                        for citation in citations:
                            ai_answer, color = _color_string(
                                ai_answer,
                                citation["start"],
                                citation["end"],
                            )
                            for doc_id in citation["document_ids"]:
                                st.session_state["cited_docs"].append(
                                    (color, rag_docs[int(doc_id[4:])])
                                )

            st.chat_message("assistant").markdown(ai_answer)

            st.session_state["messages_push"] += [
                {"role": "human", "message": user_query},
                {"role": "ai", "message": ai_answer},
            ]

    with container2:
        for i, doc in enumerate(st.session_state["cited_docs"]):
            with st.expander(f":{doc[0]}[Citation {i+1}]"):
                st.json(doc[1])
