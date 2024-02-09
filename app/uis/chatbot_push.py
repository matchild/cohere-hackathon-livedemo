import streamlit as st

from app.agents.push import AiAgent


def chat_ui_push() -> None:
    """Chatbot UI for push chat"""

    if "init_push" not in st.session_state:
        st.session_state["init_push"] = True
        st.session_state["messages_push"] = []

    st.title("Push Chat 📬")

    for message in st.session_state["messages_push"]:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    user_query = st.chat_input("Ask something...")
    if user_query:
        st.chat_message("user").markdown(user_query)

        with st.spinner("Thinking..."):
            with st.session_state["conn"].session as db_session:
                agent = AiAgent(db=db_session)
                ai_answer = agent.run(
                    user_query, chat_history=st.session_state["messages_push"]
                )

        st.chat_message("assistant").markdown(ai_answer)

        st.session_state["messages_push"] += [
            {"role": "human", "message": user_query},
            {"role": "ai", "message": ai_answer},
        ]
