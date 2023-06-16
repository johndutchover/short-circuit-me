import datetime
import os
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pandas import DataFrame
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pathlib

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


def increase_counter(message_type: str, user_id: str):
    message_counts_df: DataFrame | Any = pd.read_csv(message_counts_path)

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

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


@app.message(r"(?:help)")
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
    increase_counter('urgent', message['user'])


@app.message(r"(?:important)")
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
    increase_counter('important', message['user'])


@app.event("message")
def handle_message(event, client):
    """
    Event handler for normal messages.
    Increments the 'normal' count.
    :param event: Event object
    :param client: Slack client
    :return: None
    """
    user_id = event["user"]
    increase_counter('normal', user_id)


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
