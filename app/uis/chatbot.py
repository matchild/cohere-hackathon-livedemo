import streamlit as st

from app.constants import SQL_DATABASE_URL
from app.push.agent import PushAgent


def ui() -> None:
    st.title("Chatbot 🤖")

    if "init_chatbot" not in st.session_state:
        st.session_state["init_chatbot"] = True
        st.session_state["messages"] = []
        st.session_state["conn"] = st.connection(
            "sqlite", type="sql", url=SQL_DATABASE_URL
        )

    for message in st.session_state["messages"]:
        with st.chat_message(message[0]):
            st.markdown(message[1])

    user_query = st.chat_input("Ask something...")
    if user_query:
        st.chat_message("user").markdown(user_query)

        with st.spinner("Thinking..."):
            with st.session_state["conn"].session as db_session:
                agent = PushAgent(db=db_session)
                ai_answer = agent.run(
                    user_query,
                    chat_conversation=st.session_state["messages"],
                )

        st.chat_message("assistant").markdown(ai_answer)

        st.session_state["messages"] += [("human", user_query), ("ai", ai_answer)]
