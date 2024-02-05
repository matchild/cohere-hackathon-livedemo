import logging

import streamlit as st

from app.uis.chatbot_push import chat_ui_push
from app.uis.chatbot_pull import chat_ui_pull

logging.basicConfig(level=logging.INFO)

available_uis = {"Push Chatbot 🤖": chat_ui_push, "Pull Chatbot 🤖": chat_ui_pull}

with st.sidebar:
    chosen_ui = st.selectbox("Choose UI", available_uis.keys(), index=1)

available_uis[chosen_ui]()
