import os
import pathlib
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.switch_page_button import switch_page

env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(env_path)


# Check password function
def check_password():
    # Check if password has been entered correctly
    if st.session_state.get("password_correct"):
        return True
    else:
        password = st.text_input("Password", type="password")
        if password == os.environ.get("PASSWORD"):
            st.session_state["password_correct"] = True
            return True
        else:
            st.error("Incorrect password")
            return False


# Prompt for password
if check_password(): # TODO: add user-based login
    # Set a flag in the session state to indicate that the password is correct
    st.session_state["password_correct"] = True
    # Redirect using extras switch_page
    switch_page('app')
