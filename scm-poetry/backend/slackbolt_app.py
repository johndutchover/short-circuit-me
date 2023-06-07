"""
Module backend.slackbolt_app

This module provides a collection of functions/classes for performing various operations.

Functions:
    - action_button_click
    - endpoint
    - handle_message_events
    - increase_notification_counters
    - message_hello
    - function_name_2: Description of function_name_2.

Classes:
    - ClassName1: Description of ClassName1.
    - ClassName2: Description of ClassName2.

Usage:
    from module_name import function_name_1, ClassName1
    ...
"""
import os
import re
import csv

from dotenv import load_dotenv
from slack_bolt import App
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

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


counter = 0

str_help = r"(?:help)"
regex_help = re.compile(str_help, flags=re.I)


@app.message(regex_help)
def increase_notification_count():
    """
    increment counter of help strings
    :return:
    """
    global counter
    counter += 1

    print(counter)


# Add middleware / listeners here
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html

str_hello = r"(?:hello)"
regex_hello = re.compile(str_hello, flags=re.I)


@app.message(regex_hello)
def message_hello(message, say):
    """
    increment counter of "hello" strings
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

    def hello_to_csv(item: message):
        """
        very basic FastAPI endpoint which writes JSON request body to a CSV file
        :param item:
        :return:
        """
        # name of csv file
        filename = "output_hello.csv"

        # writing to csv file
        with open(filename, 'a') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=['user', 'ts', 'text'])

            # writing headers (field names) if the file is new/empty
            if os.stat(filename).st_size == 0:
                writer.writeheader()

            # writing data rows
            writer.writerow({k: item.get(k) for k in ['user', 'ts', 'text']})

        return {"success": True}

    hello_to_csv(message)


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
