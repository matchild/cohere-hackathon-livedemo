import streamlit as st

from app.agents.push import AiAgent
from app.constants import SQL_DATABASE_URL


def chat_ui_pull() -> None:
    st.title("Pull Chatbot 🤖")

    col1, col2= st.columns(2)

    with col1:
        if "init_chatbot" not in st.session_state:
            st.session_state["init_chatbot"] = True
            st.session_state["messages"] = []
            st.session_state["conn"] = st.connection(
                "sqlite", type="sql", url=SQL_DATABASE_URL
            )

        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

        user_query = st.chat_input("Ask something...")
        if user_query:
            st.chat_message("user").markdown(user_query)

            with st.spinner("Thinking..."):
                with st.session_state["conn"].session as db_session:
                    agent = AiAgent(db=db_session)
                    ai_answer = agent.run(
                        user_query, chat_history=st.session_state["messages"]
                    )

            st.chat_message("assistant").markdown(ai_answer)

            st.session_state["messages"] += [
                {"role": "human", "message": user_query},
                {"role": "ai", "message": ai_answer},
            ]

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")



