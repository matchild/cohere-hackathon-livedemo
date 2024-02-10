import streamlit as st


def st_chat_containers(
    subtitle_left: str, subtitle_right: str, chat_label: str = "Ask something..."
) -> tuple:

    _CONTAINER_HEIGHT = 400

    col_left, col_right = st.columns(2)

    with col_left:
        st.header(subtitle_left)
        container_left = st.container(height=_CONTAINER_HEIGHT)
        chat_input = st.chat_input(chat_label)

    with col_right:
        st.header(subtitle_right)
        container_right = st.container(height=_CONTAINER_HEIGHT)

    return container_left, container_right, chat_input
