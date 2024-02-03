import streamlit as st


def ui() -> None:
    st.title("Chatbot 🤖")

    if "init_chatbot" not in st.session_state:
        st.session_state["init_chatbot"] = True
        st.session_state["messages"] = []

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Ask something...")
    if user_query:
        st.chat_message("user").markdown(user_query)

        with st.spinner("Thinking..."):
            ai_answer = user_query  # mirror bot

        st.chat_message("assistant").markdown(ai_answer)

        st.session_state["messages"] += [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_answer},
        ]
