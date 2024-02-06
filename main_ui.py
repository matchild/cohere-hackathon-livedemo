import logging

import streamlit as st

from app.constants import SQL_DATABASE_URL
from app.uis.chatbot_pull import chat_ui_pull
from app.uis.chatbot_push import chat_ui_push

logging.basicConfig(level=logging.INFO)

available_uis = {"Push Chatbot 🤖": chat_ui_push, "Pull Chatbot 🤖": chat_ui_pull}

if "init_main" not in st.session_state:
    st.session_state["init_main"] = True
    st.session_state["conn"] = st.connection("sqlite", type="sql", url=SQL_DATABASE_URL)

with st.sidebar:
    chosen_ui = st.selectbox("Choose UI", available_uis.keys(), index=1)

available_uis[chosen_ui]()
