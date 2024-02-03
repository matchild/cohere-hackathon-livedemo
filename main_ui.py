import streamlit as st

from app.uis.chatbot import ui

available_uis = {"Chatbot 🤖": ui}

with st.sidebar:
    chosen_ui = st.selectbox("Choose UI", available_uis.keys())

available_uis[chosen_ui]()
