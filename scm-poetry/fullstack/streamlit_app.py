import os
import streamlit as st
from dotenv import load_dotenv
from streamlit.runtime.state import SessionState
from streamlit_extras.switch_page_button import switch_page

load_dotenv('env')


def login_page(session):
    password = st.text_input("Password", type="password")
    if password == "secret":
        session.authenticated = True
        session.page = "protected"


def protected_page():
    st.write("This is the protected page. Only authenticated users can access this.")


def main():
    session_state = SessionState.get(authenticated=False, page="login")

    if session_state.page == "login":
        login_page(session_state)
    elif session_state.page == "protected" and session_state.authenticated:
        protected_page()
    else:
        st.write("Invalid page or authentication failed.")


if __name__ == "__main__":
    main()


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
    switch_page("app")
