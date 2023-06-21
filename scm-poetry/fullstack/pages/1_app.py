import os
import pathlib
from datetime import datetime

import pandas as pd
import pytz
import streamlit as st
from bokeh.models import FuncTickFormatter
from bokeh.plotting import figure
from pandas.errors import EmptyDataError

current_utc_time = datetime.utcnow()
local_timezone = pytz.timezone('America/New_York')  # Replace 'America/New_York' with your desired time zone
current_local_time = current_utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

st.set_page_config(page_title="Dashboard", page_icon="✅")

st.write('Current local time:', current_local_time)

envdir = pathlib.Path(__file__).parent
env_dir_path = envdir / ".env"

cfd = pathlib.Path(__file__).parent.parent
message_counts_path = os.getenv('MESSAGE_COUNTS_PATH', cfd / "message_counts.csv")

st.title('Notification Dashboard')
st.subheader('Slack :zap: :blue[message] summary')

try:
    df_messages = pd.read_csv(message_counts_path, header='infer', encoding='utf-8')

    # Convert msg_date to datetime
    df_messages['msg_date'] = pd.to_datetime(df_messages['msg_date'])
    st.table(df_messages)

    # Bokeh plot with a title and axis labels
    p = figure(title="Bokeh plot", x_axis_label='Date', y_axis_label='Messages', x_axis_type="datetime")
    p.line(df_messages['msg_date'], df_messages['normal'], legend_label="Normal", color="green", line_width=2)
    p.line(df_messages['msg_date'], df_messages['important'], legend_label="Important", color="orange", line_width=2)
    p.line(df_messages['msg_date'], df_messages['urgent'], legend_label="Critical", color="red", line_width=2)

    # Display the Bokeh plot using Streamlit
    st.bokeh_chart(p, use_container_width=True)

    # Define custom tick formatter to display day of the week
    code = """
    var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var date = new Date(tick);
    var localDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
    var day = localDate.getDay();
    return days[day];
    """
    p.xaxis.formatter = FuncTickFormatter(code=code)

    # Plot an area chart
    st.area_chart(df_messages.set_index('msg_date')[['normal', 'important', 'urgent']])

except EmptyDataError:
    st.text('INFO: The message_counts.csv file is empty')
