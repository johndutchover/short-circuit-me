# https://docs.streamlit.io/library/get-started/create-an-app

import streamlit as st


def get_important_notifications():
    return 42

st.title('Notification Overview Dashboard')

st.text(f'You got {get_important_notifications()} important notifications.')

'''To run this file with poetry here are the commands:
        poetry shell
        streamlit run short_circuit_me.py
    Then type "code ." to launch VSCode
'''