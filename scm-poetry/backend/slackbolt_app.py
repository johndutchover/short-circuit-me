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


from dotenv import load_dotenv
from fastapi import FastAPI
from motor import motor_asyncio
from pydantic import BaseModel
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pathlib

from starlette.requests import Request

cfd = pathlib.Path(__file__).parent
message_counts_path = cfd / "message_counts.csv"

load_dotenv()  # read local .env file


# Define the data model
class Item(BaseModel):
    date: str
    count1: int
    flag: int
    count2: int


# MongoDB Atlas connection string
uri = os.environ.get("POETRY_MONGODB_URL")

# Set the Stable API version when creating a new client
client = motor_asyncio.AsyncIOMotorClient(os.environ["POETRY_MONGODB_URL"])
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


@api.post("/slack/events")
async def endpoint(req: Request):
    """
    endpoint which handles incoming requests from Slack
    :param req:
    :return:
    """
    return await app_handler.handle(req)


async def increase_counter(message_type: str):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    current_data = await collection.find_one({"date": formatted_date})

    if current_data is None:
        new_data = {
            "date": formatted_date,
            "normal": 0,
            "important": 0,
            "urgent": 0
        }
        await collection.insert_one(new_data)
    else:
        new_data = current_data

    new_data[message_type] += 1
    await collection.replace_one({"date": formatted_date}, new_data)


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
async def message_urgent(message, say):
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


@app.message(regex_p2)
async def message_important(message, say):
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
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "This better be important"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.event("message")
async def handle_message_events(body, logger):
    """
    handle Slack message events
    :param body:
    :param logger:
    :return:
    """
    logger.info(body)
    await increase_counter('normal')


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"]).start()
