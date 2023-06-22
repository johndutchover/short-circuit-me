import datetime
import os
import pathlib
import re
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pandas import DataFrame
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

cfd = pathlib.Path(__file__).parent.parent
message_counts_path = os.getenv('MESSAGE_COUNTS_PATH', cfd / "message_counts.csv")

load_dotenv()  # read local .env file

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET")  # not required for socket mode
)
app_handler = SlackRequestHandler(app)

# Initialize a contact dictionary
contacts = {}

bots_clientid = os.getenv('POETRY_SCM_BOT_CLIENTID')

# Users who are allowed to use the commands
allowed_users = ["USLACKBOT", bots_clientid]


# Slash command that adds a contact
@app.command("/addcontact")
def add_contact(ack, respond, command):
    # Acknowledge command request
    ack()

    # Get user's ID from the command text
    user_id = command['text']

    provided_id_has_correct_format = re.match("^U[A-Z0-9]{8,}$", user_id)
    if provided_id_has_correct_format:
        # Add user to contacts
        contacts[user_id] = user_id
        # Respond with success message
        respond(f"User {user_id} added to contacts.")
    else:
        respond("Invalid format. Please provide a valid Slack User ID.")


# Slash command that retrieves a contact
@app.command("/getcontact")
def get_contact(ack, respond, command):
    # Acknowledge command request
    ack()

    user_id = command['text']
    if user_id in contacts:
        respond(f"Contact found for User ID: {contacts[user_id]}")
    else:
        respond(f"No contact found for User ID: {user_id}")


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


api = FastAPI()

if os.path.exists(message_counts_path) and os.stat(message_counts_path).st_size > 0:
    message_counts = pd.read_csv(message_counts_path)
else:
    message_counts = pd.DataFrame(columns=["level_0", "normal", "important", "urgent"])

message_counts.rename(columns={"level_0": "msg_date"}, inplace=True)

message_counts.to_csv(message_counts_path, index=False)


@api.post("/slack/events")
async def endpoint(req: Request):
    """
    Endpoint which handles incoming requests from Slack.
    :param req: Request object
    :return: Awaitable response
    """
    return await app_handler.handle(req)


@api.get("/slack/install")
async def install(req: Request):
    return await app_handler.handle(req)


def increase_counter(message_type: str):
    message_counts_df: DataFrame | Any = pd.read_csv(message_counts_path)

    now = datetime.datetime.now()
    formatted_date = now.date().strftime("%Y-%m-%d")

    # Check if the date already exists in the DataFrame
    if formatted_date in message_counts_df['msg_date'].values:
        # Update the count of the corresponding message_type
        message_counts_df.loc[
            message_counts_df['msg_date'] == formatted_date,
            message_type
        ] += 1
    else:
        # Create a new row with zeros
        new_row = pd.DataFrame(
            {
                "msg_date": formatted_date,
                "normal": 0,
                "important": 0,
                "urgent": 0
            },
            index=[0]
        )
        # Increment the count of the corresponding message_type
        new_row[message_type] += 1
        message_counts_df = pd.concat([message_counts_df, new_row], ignore_index=True)

    message_counts_df.to_csv(message_counts_path, index=False)


@app.message(re.compile("(asap|help|urgent)", re.I))
def message_urgent(message, say):
    """
    Increment counter of Priority 1 (urgent) string matches.
    Say() sends a message to the channel where the event was triggered.
    :param message: Message object
    :param say: Say function
    :return: None
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
    increase_counter('urgent')


@app.message(re.compile("(important|need|soon)", re.I))
def message_important(message, say):
    """
    Increment counter of Priority 2 (important) string matches.
    Say() sends a message to the channel where the event was triggered.
    :param message: Message object
    :param say: Say function
    :return: None
    """
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{message['user']}> Can it wait until Monday?"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click to record a message"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Please record at this time <@{message['user']}>!"
    )
    increase_counter('important')


@app.message(re.compile("(hi|hello|hey)", re.I))
def say_hello_regex(say, context):
    # regular expression matches are inside of context.matches
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")
    increase_counter('normal')


@app.action("button_click")
def action_button_click(body, ack, say):
    """
    Acknowledge the action.
    :param body: Action payload
    :param ack: Acknowledge function
    :param say: Say function
    :return: None
    """
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"])
    handler.start()
