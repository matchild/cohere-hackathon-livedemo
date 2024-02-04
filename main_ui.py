import logging

import streamlit as st

from app.uis.chatbot import ui

logging.basicConfig(level=logging.INFO)

available_uis = {"Chatbot 🤖": ui}

with st.sidebar:
    chosen_ui = st.selectbox("Choose UI", available_uis.keys())

available_uis[chosen_ui]()
