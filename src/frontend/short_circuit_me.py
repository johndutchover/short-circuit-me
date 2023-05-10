# https://docs.streamlit.io/library/get-started/create-an-app

import streamlit as st


def get_important_notifications():
    return 42

st.title('Notification Overview Dashboard')

st.text(f'You got {get_important_notifications()} important notifications.')

# run this file via: streamlit run short_circuit_me.py