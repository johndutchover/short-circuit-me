"""This module provides frontend web functionality

        Author: John Dutchover

        Functions:
        - list

        Usage:
        - tbd
"""
import os
import pathlib
from datetime import datetime

import pandas as pd
import pymongo
import pytz
import streamlit as st
from bokeh.models import FuncTickFormatter
from bokeh.plotting import figure
from pandas.errors import EmptyDataError
from pymongo import MongoClient

envdir = pathlib.Path(__file__).parent
env_dir_path = envdir / ".env"

# MongoDB connection string
uri = os.environ.get("POETRY_MONGODB_URL")

st.set_page_config(page_title="Dashboard", page_icon="✅")

if not st.session_state.get("password_correct"):
    st.write("Please login :)")

else:
    # Initialize connection.
    # Uses st.cache_resource to only run once.
    @st.cache_resource
    def init_connection():
        """

        :return:
        :rtype:
        """
        return pymongo.MongoClient(**st.secrets.db_credentials)


    client_init = init_connection()

    client = MongoClient(uri)

    db = client["messagesdb"]
    collection = db["slackcoll"]

    # Convert MongoDB documents to DataFrame
    df_messages = pd.DataFrame(list(collection.find()))

    print(df_messages.head())  # Check the first few rows of the DataFrame
    print(df_messages.info())  # Print information about the DataFrame


    # Only include documents where 'field1' is 'value1', and only include 'field2' and 'field3' in the output
    # df_messages = pd.DataFrame(list(collection.find({'field1': 'value1'}, {'field2': 1, 'field3': 1})))

    # Pull data from the collection.
    # Uses st.cache_data to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def get_data():
        """

        :return:
        :rtype:
        """
        db1 = client["messagesdb"]
        item = db1.slackcoll.find()
        item = list(item)  # make hashable for st.cache_data
        return item


    items = get_data()

    current_utc_time = datetime.utcnow()
    local_timezone = pytz.timezone(
        "America/New_York"
    )  # Replace 'America/New_York' with your desired time zone
    current_local_time = current_utc_time.replace(tzinfo=pytz.utc).astimezone(
        local_timezone
    )

    st.write("Current local time:", current_local_time)

    envdir = pathlib.Path(__file__).parent
    env_dir_path = envdir / ".env"

    st.title("Notification Dashboard")
    st.subheader("Slack :zap: :blue[message] summary")

    try:
        df_messages = pd.DataFrame(list(collection.find({}, {"_id": 0})))
        print(df_messages.columns)
        st.table(df_messages)

        # Convert msg_date to datetime format if needed
        df_messages["msg_date"] = pd.to_datetime(df_messages["msg_date"])

        # Bokeh plot with a title and axis labels
        p = figure(
            title="Bokeh plot of Messages",
            x_axis_label="Date",
            y_axis_label="Messages",
            x_axis_type="datetime",
        )
        p.line(
            df_messages["msg_date"],
            df_messages["normal"],
            legend_label="Normal",
            color="green",
            line_width=2,
        )
        p.line(
            df_messages["msg_date"],
            df_messages["priority"],
            legend_label="Priority",
            color="orange",
            line_width=2,
        )
        p.line(
            df_messages["msg_date"],
            df_messages["urgent"],
            legend_label="Critical",
            color="red",
            line_width=2,
        )

        # Define custom tick formatter to display day of the week
        CODE = """
        var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        var date = new Date(tick);
        var localDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
        var day = localDate.getDay();
        return days[day];
        """
        p.xaxis.formatter = FuncTickFormatter(code=CODE)

        # Display the Bokeh plot using Streamlit
        st.bokeh_chart(p, use_container_width=True)

        # Plot an area chart
        st.area_chart(
            df_messages.set_index("msg_date", inplace=True),
            df_messages[["normal", "priority", "urgent"]]
        )

    except EmptyDataError:
        st.text("INFO: Database is empty")
