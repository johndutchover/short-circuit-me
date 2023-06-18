import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.switch_page_button import switch_page

load_dotenv('.env')


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
if not check_password():
    st.stop()

if check_password():
    switch_page("home")
