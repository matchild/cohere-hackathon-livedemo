import streamlit as st

# TODO: exchange with pull agent
from app.agents.push import AiAgent
from app.db.services import get_dataframe_by_id


def chat_ui_pull() -> None:
    """Chatbot UI for pull chat"""

    _CONTAINER_HEIGHT = 600

    if "init_pull" not in st.session_state:
        st.session_state["init_pull"] = True
        st.session_state["messages_pull"] = []

    st.title("Pull Chatbot 🤖")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Chat")

        container1 = st.container(height=_CONTAINER_HEIGHT)

        for message in st.session_state["messages_pull"]:
            container1.chat_message(message["role"]).markdown(message["message"])

        user_query = st.chat_input("Ask something...")
        if user_query:
            container1.chat_message("user").markdown(user_query)

            with st.spinner("Thinking..."):
                with st.session_state["conn"].session as db_session:
                    agent = AiAgent(db=db_session)
                    ai_answer = agent.run(
                        user_query, chat_history=st.session_state["messages_pull"]
                    )

            container1.chat_message("assistant").markdown(ai_answer)

            st.session_state["messages_pull"] += [
                {"role": "human", "message": user_query},
                {"role": "ai", "message": ai_answer},
            ]

    with col2:
        st.header("Database")

        container2 = st.container(height=_CONTAINER_HEIGHT)
        with st.session_state["conn"].session as db_session:
            # TODO: use the right objects here
            db_object = get_dataframe_by_id(db=db_session, id=1)

            obj_container = container2.container(border=True)
            obj_container.write("Registered object:")
            obj_container.json(
                {
                    "id": db_object.id,
                    "name": db_object.name,
                    "description": db_object.description,
                    "registered_at": db_object.registered_at,
                }
            )
