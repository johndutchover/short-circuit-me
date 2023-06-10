"""
Module backend.slackbolt_app

This module provides a collection of functions/classes for performing various operations.

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
from fastapi import FastAPI, Request
from pandas import DataFrame
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()  # read local .env file


# Define the data model
class Item(BaseModel):
    date: str
    count1: int
    flag: int
    count2: int


load_dotenv()  # read local .env file
# MongoDB Atlas connection string
uri = os.environ.get("POETRY_MONGODB_URL")

# Set the Stable API version when creating a new client
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
# database name in MongoDB
db = client["messagesdb"]
# collection name in MongoDB
collection = db["slackcoll"]

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    # signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET") # not required for socket mode
)
app_handler = SlackRequestHandler(app)
api = FastAPI()

if os.path.exists("../data/message_counts.csv"):
    message_counts = pd.read_csv("../data/message_counts.csv")
else:
    message_counts = pd.DataFrame(columns=["normal", "important", "urgent"])
    message_counts.to_csv("../data/message_counts.csv")

'''
# Define a POST method for creating a MongoDB document
@api.post("/items/")
async def create_item(item: Item):
    # Convert the item to a dict so it can be stored in MongoDB
    item_dict = item.dict()
    result = collection.insert_one(item_dict)
    return {"inserted_id": str(result.inserted_id)}
'''


@api.post("/slack/events")
async def endpoint(req: Request):
    """
    endpoint which handles incoming requests from Slack
    :param req:
    :return:
    """
    return await app_handler.handle(req)


def increase_counter(message_type: str):
    message_counts_df: DataFrame | Any = pd.read_csv("../data/message_counts.csv", index_col=0)

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    if formatted_date not in message_counts_df.index:
        message_counts_df.loc[formatted_date] = [0, 0, 0]

    message_counts_df.loc[formatted_date, message_type] += 1
    message_counts_df.to_csv("../data/message_counts.csv")


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
