import pathlib
import pandas as pd
import streamlit as st

from bokeh.plotting import figure
from dotenv import load_dotenv
from pandas.errors import EmptyDataError

if 'key' not in st.session_state:
    st.session_state.key = 'shared'

st.set_page_config(page_title="Dashboard", page_icon="✅")

load_dotenv('../.env')

cfd = pathlib.Path(__file__).parent.parent
message_counts_path = cfd / "message_counts.csv"


def get_important_notifications():
    return 42


def get_critical_notifications():
    return 7


# page title
st.title('Slack Notification Dashboard')
# body st.text(f'You got {get_important_notifications()} important and {get_critical_notifications()} critical
# notifications.')
st.subheader('Slack :zap: :blue[notification] summary')

try:
    df_messages = pd.read_csv(message_counts_path, header='infer')
    st.table(df_messages)
except EmptyDataError:
    st.text('INFO: The message_counts.csv file is empty')

df_weekly = pd.DataFrame({
    'important_messages': [1, 2, 3, 4, 3, 2, 3],
    'normal_messages': [10, 20, 30, 40, 22, 29, 30],
    'critical_messages': [0, 2, 3, 4, 3, 4, 3],
    'days': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
})

# prepare some data
x1 = [10, 20, 30, 40, 30, 50, 40]
y1 = [1, 2, 3, 4, 3, 2, 3]
y2 = [10, 20, 30, 40, 22, 29, 30]
y3 = [0, 2, 3, 4, 3, 4, 3]

# widget (slider)
values = st.slider(
    'Select a range of messages to include',
    0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

# bokeh: create a new plot with a title and axis labels
p = figure(title="Bokeh plot", x_axis_label='messages', y_axis_label='day')
# add multiple renderers
p.line(x1, y1, legend_label="Important", color="blue", line_width=2)
p.line(x1, y2, legend_label="Normal", color="green", line_width=2)
p.line(x1, y3, legend_label="Critical", color="red", line_width=2)
st.bokeh_chart(p, use_container_width=True)

# st.area chart
st.area_chart(
    df_weekly,
    x="important_messages",
    y="days"
)

# '''To run this file:
# - from VSCode, use "Run Python File" instead of "Run Code" (properly activates venv)
# - from PyCharm...set default python interpreter to venv
# - from external terminal, use `poetry shell` followed by:
#  - `streamlit run streamlit_csv.py`'''
