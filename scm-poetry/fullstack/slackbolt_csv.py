"""
Module backend.slackbolt_csv

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
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from pandas import DataFrame
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pathlib

from starlette.requests import Request

cfd = pathlib.Path(__file__).parent
message_counts_path = cfd / "message_counts.csv"

load_dotenv()  # read local .env file

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET")  # not required for socket mode
)
app_handler = SlackRequestHandler(app)

# Fetch users list using Bolt method
response = app.client.users_list()

# create dict literal and assign users
user_data = {'users': response['members']}


# Now, 'user_dict' contains a 'users' key whose value is a list of users.

def find_user_by_id(user_id):
    for user in user_data['users']:
        if user['id'] == user_id:
            return user


api = FastAPI()

if os.path.exists(message_counts_path):
    message_counts = pd.read_csv(message_counts_path)
    message_counts.set_index(['date', 'user_id'], inplace=True)
else:
    message_counts = pd.DataFrame(columns=["date", "user_id", "normal", "important", "urgent"])
    message_counts.set_index(['date', 'user_id'], inplace=True)
    message_counts.to_csv(message_counts_path)


@api.post("/slack/events")
async def endpoint(req: Request):
    """
     endpoint which handles incoming requests from Slack
     :param req:
     :return:
     """
    return await app_handler.handle(req)


def increase_counter(message_type: str, user_id: str):
    message_counts_df: DataFrame | Any = pd.read_csv(message_counts_path)
    message_counts_df.set_index(['date', 'user_id'], inplace=True)

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    # Check if the date-user_id combination already exists
    if (formatted_date, user_id) not in message_counts_df.index:
        # Create a new row with zeros
        message_counts_df.loc[(formatted_date, user_id), :] = [0, 0, 0]

    # Increase the count of the corresponding message_type
    message_counts_df.loc[(formatted_date, user_id), message_type] += 1

    message_counts_df.reset_index().to_csv(message_counts_path, index=False)


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
                "text": {"type": "mrkdwn", "text": f"Do you need help <@{message['user']}>?"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click to escalate"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )
    increase_counter('urgent', message['user'])


@app.message(regex_p2)
def message_urgent(message, say):
    """
    increment counter of Priority 2 (important) string matches
    say() sends a message to the channel where the event was triggered
    :param message:
    :param say:
    :return:
    """
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{message['user']}>Can it wait until Monday?"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click to record a message"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Please record at ths tone <@{message['user']}>!"
    )
    increase_counter('important', message['user'])


@app.event("message")
def handle_message(event, client):
    # Grab the sender's user id
    user_id = event["user"]
    increase_counter('normal', event["user"])


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
