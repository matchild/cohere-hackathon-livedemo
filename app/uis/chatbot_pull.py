import streamlit as st

# TODO: exchange with pull agent
from app.agents.push import AiAgent


def chat_ui_pull() -> None:
    """Chatbot UI for pull chat"""

    if "init_pull" not in st.session_state:
        st.session_state["init_pull"] = True
        st.session_state["messages_pull"] = []

    st.title("Pull Chatbot 🤖")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Chat")

        for message in st.session_state["messages_pull"]:
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

        user_query = st.chat_input("Ask something...")
        if user_query:
            st.chat_message("user").markdown(user_query)

            with st.spinner("Thinking..."):
                with st.session_state["conn"].session as db_session:
                    agent = AiAgent(db=db_session)
                    ai_answer = agent.run(
                        user_query, chat_history=st.session_state["messages_pull"]
                    )

            st.chat_message("assistant").markdown(ai_answer)

            st.session_state["messages_pull"] += [
                {"role": "human", "message": user_query},
                {"role": "ai", "message": ai_answer},
            ]

    with col2:
        st.header("Database")
        # with st.session_state["conn"].session as db_session:
        #     st.write(get_dataframe_by_id(db=db_session, id=1).description)
