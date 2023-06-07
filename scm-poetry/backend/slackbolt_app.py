"""
Module backend.slackbolt_app

This module provides a collection of functions/classes for performing various operations.

Functions:
    - action_button_click
    - endpoint
    - handle_message_events
    - increase_notification_counters
    - message_normal
    - function_name_2: Description of function_name_2.

Classes:
    - ClassName1: Description of ClassName1.
    - ClassName2: Description of ClassName2.

Usage:
    from module_name import function_name_1, ClassName1
    ...
"""
import datetime
import os
import re
import csv

import pandas as pd
from dotenv import load_dotenv
from slack_bolt import App
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

from typing import Literal

load_dotenv()  # read local .env file

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

if file exists "message_counts":
    message_counts = pd.read_csv("message_counts.csv")
else:
    message_counts = pd.DataFrame(columns=["normal", "important", "urgent"])
    message_counts.to_csv("message_counts.csv")

def increase_counter(message_type: str):  # Literal["normal", "important", "urgent"]

    message_counts = pd.read_csv("message_counts.csv")

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    if formatted_date not in message_counts.index:
        message_counts.loc[formatted_date, :] = 0

    message_counts.loc[formatted_date, message_type] += 1
    message_counts.to_csv("message_counts.csv")


counter = 0
counter_important = 0
counter_urgent = 0

# Add middleware / listeners here
# args here: https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html

str_p1 = r"(?:help)"
regex_p1 = re.compile(str_p1, flags=re.I)


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

    def increase_urgent_count():
        """
        increment counter of Priority 1 (urgent) string matches
        :return:
        """
        global counter_urgent  # TODO temporary use of global for POC
        counter_urgent += 1

        print("Urgent message logged: ", counter_urgent)

    def urgent_to_csv(item: message):
        """
        very basic FastAPI endpoint which writes JSON request body to a CSV file
        :param item:
        :return:
        """
        # name of csv file
        filename = "output_urgent.csv"

        # writing to csv file
        with open(filename, 'a') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=['user', 'channel', 'text'])

            # writing headers (field names) if the file is new/empty
            if os.stat(filename).st_size == 0:
                writer.writeheader()

            # writing data rows
            writer.writerow({k: item.get(k) for k in ['user', 'channel', 'text']})

        return {"success": True}

    urgent_to_csv(message)
    # increase_urgent_count()
    increase_counter(message_type="urgent")

str_p2 = r"(?:important)"
regex_p2 = re.compile(str_p2, flags=re.I)


@app.message(regex_p2)
def message_important(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click if important"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

    def increase_important_count():
        """
        increment counter of Priority 2 (important) string matches
        :return:
        """
        global counter_important  # TODO temporary use of global for POC
        counter_important += 1

        print("Important message logged: ", counter_important)

    # increase_important_count()
    increase_counter(message_type="important")


str_p3 = r"(?:hello)"
regex_p3 = re.compile(str_p3, flags=re.I)


@app.message(regex_p3)
def message_normal(message, say):
    """
    increment counter of Priority 3 (normal) string matches
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
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

    print("Hello")

    def normal_to_csv(item: message):
        """
        very basic FastAPI endpoint which writes JSON request body to a CSV file
        :param item:
        :return:
        """
        # name of csv file
        filename = "output_normal.csv"

        # writing to csv file
        with open(filename, 'a') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=['user', 'channel', 'text'])

            # writing headers (field names) if the file is new/empty
            if os.stat(filename).st_size == 0:
                writer.writeheader()

            # writing data rows
            writer.writerow({k: item.get(k) for k in ['user', 'channel', 'text']})

        return {"success": True}

    normal_to_csv(message)


@app.event("message")
def handle_message_events(body, logger):
    """
    hangle Slack message events
    :param body:
    :param logger:
    :return:
    """
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

# Start the Bolt app
# if __name__ == "__main__":
#    app.start(port=3000)
#    app.start(port=int(os.environ.get("PORT", 3000)))
