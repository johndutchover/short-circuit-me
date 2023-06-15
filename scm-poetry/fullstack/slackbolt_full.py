"""
Module backend.slackbolt_full

asynchronous Python backend for a Slack bot, utilizing the Slack Bolt and FastAPI frameworks

Functions:
    - endpoint(req)
    - handle_message_events(body, logger)
    - increase_counter(message_type)
    - message_urgent(message, say)

Classes:
    - N/A

Usage:
    from module_name import function_name_1, ClassName1
    ...
"""
import datetime
import os
import re
import pymongo
from typing import Any

import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pandas import DataFrame
from pandas.errors import EmptyDataError
from pymongo import MongoClient
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pathlib

load_dotenv()

# MongoDB Atlas connection string
uri = os.environ.get("POETRY_MONGODB_URL")

# Connect to MongoDB Atlas
client = MongoClient(os.environ["POETRY_MONGODB_URL"])

cfd = pathlib.Path(__file__).parent
message_counts_path = cfd / "message_counts.csv"

st.set_page_config(page_title="Simple Dashboard", page_icon="✅")


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets.db_credentials)


client_init = init_connection()

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    # signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET") # not required for socket mode
)
app_handler = SlackRequestHandler(app)
api = FastAPI()

if os.path.exists(message_counts_path):
    message_counts = pd.read_csv(message_counts_path)
else:
    message_counts = pd.DataFrame(columns=["normal", "important", "urgent"])
    message_counts.to_csv(message_counts_path)


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client["messagesdb"]
    items = db.mycollection.find()
    items = list(items)  # make hashable for st.cache_data
    return items


items = get_data()


def get_important_notifications():
    return 42


def get_critical_notifications():
    return 7


# page title
st.title('Notification Overview Dashboard')
# body st.text(f'You got {get_important_notifications()} important and {get_critical_notifications()} critical
# notifications.')
st.subheader('Slack :zap: :blue[notification] summary')

try:
    df_messages = pd.read_csv("message_counts.csv", header='infer')
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


@api.post("/slack/events")
async def endpoint(req: Request):
    """
     endpoint which handles incoming requests from Slack
     :param req:
     :return:
     """
    return await app_handler.handle(req)


def increase_counter(message_type: str):
    message_counts_df: DataFrame | Any = pd.read_csv(message_counts_path, index_col=0)

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    if formatted_date not in message_counts_df.index:
        message_counts_df.loc[formatted_date] = [0, 0, 0]

    message_counts_df.loc[formatted_date, message_type] += 1
    message_counts_df.to_csv(message_counts_path)


counter = 0
counter_important = 0
counter_urgent = 0

# Add middleware / listeners here
# args here: https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html

str_p1 = r"(?:help)"
regex_p1 = re.compile(str_p1, flags=re.I)
str_p2 = r"(?:important)"
regex_p2 = re.compile(str_p2, flags=re.I)
str_p3 = r"(?:hello)"
regex_p3 = re.compile(str_p3, flags=re.I)


@app.message(regex_p1)
def message_urgent(message, say):
    """
    increment counter of Priority 1 (urgent) string matches
    say() sends a message to the channel where the event was triggered
    :param message:
    :param say:
    :return:
    """
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click to escalate"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )
    increase_counter('urgent')


@app.event("message")
def handle_message_events(body, logger):
    """
    hangle Slack message events
    :param body:
    :param logger:
    :return:
    """
    increase_counter('normal')
    logger.info(body)


@app.action("button_click")
def action_button_click(body, ack, say):
    """
    Acknowledge the action
    :param body:
    :param ack:
    :param say:
    :return:
    """
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"]).start()
