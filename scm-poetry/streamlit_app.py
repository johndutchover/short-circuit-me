# https://docs.streamlit.io/library/get-started/create-an-app
# .io/how-to-build-a-real-time-live-dashboard-with-streamlit/#2-how-to-do-a-basic-dashboard-setup

#If you are using Streamlit version 1.10.0 or higher, your main script should live in a directory other than the root directory. 
# When using Docker, you can use the WORKDIR command to specify the directory where your main script lives.

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Simple Dashboard",
    page_icon="✅",
    layout="centered",
)

def get_important_notifications():
    return 42

df = pd.DataFrame({
  'Important messages': [1, 2, 3, 4],
  'Total messages': [10, 20, 30, 40]
})

df_weekly = pd.DataFrame({
  'Important messages': [1, 2, 3, 4, 3, 2, 3],
  'Normal messages': [10, 20, 30, 40, 220, 29, 30],
  'Critical messages': [0, 2, 3, 4, 3, 4, 3],
})

# page title
st.title('Notification Overview Dashboard')
# body
st.text(f'You got {get_important_notifications()} important notifications.')
# call dataframe
df
# widget (slider)
x = st.slider('x') 
st.write(x, 'Short-circuit-me power level is', x * x)

st.header("Bar Chart")
days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
st.bar_chart(data=df_weekly,x=days)

#'''To run this file:
#- from VSCode, use "Run Python File" instead of "Run Code" (properly activates venv)
#- from PyCharm...set default python interpreter to venv
#- from external terminal, use `poetry shell` followed by:
#  - `streamlit run streamlit_app.py`'''
