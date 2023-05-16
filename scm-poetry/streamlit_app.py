# https://docs.streamlit.io/library/get-started/create-an-app

import streamlit as st

st.set_page_config(
    page_title="Simple Dashboard",
    page_icon="✅",
    layout="wide",
)

def get_important_notifications():
    return 42


st.title('Notification Overview Dashboard')

st.text(f'You got {get_important_notifications()} important notifications.')

'''To run this file:
        - from VSCode, use "Run Python File" instead of "Run Code" (properly activates venv)
        - from PyCharm...it will probably just work fine.
        - from external terminal, use "poetry shell" followed by:
            streamlit run short_circuit_me.py
'''
