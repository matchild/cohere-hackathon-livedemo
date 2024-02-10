import logging

import streamlit as st

from app.constants import SQL_DATABASE_URL
from app.uis.chatbot_pull import chat_ui_pull
from app.uis.chatbot_push import chat_ui_push
from app.uis.welcome_page import welcome_ui

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="CoDA | Cohere Database Assistant", page_icon="🤖", layout="wide"
)

if "init_main" not in st.session_state:
    st.session_state["init_main"] = True
    st.session_state["conn"] = st.connection("sqlite", type="sql", url=SQL_DATABASE_URL)

tab_info, tab_pull, tab_push = st.tabs(
    ["Welcome Page 👋", "Data Submission 📮", "Data Retrieval 📬"]
)

with tab_info:
    welcome_ui()
with tab_pull:
    chat_ui_pull()
with tab_push:
    chat_ui_push()
